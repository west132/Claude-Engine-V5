# Copyright (c) 2026 West132.WL. All rights reserved.
"""One player turn, start to finish (engine §2 loop), with code in charge of the process.

triage → LOAD → referee tool loop (model judges, host computes) → narrator → checker →
PERSIST (GM-Δ block, journal) → checkpoint save when due. State changes are transactional:
any failure before the commit restores the campaign exactly as it was.
"""
from __future__ import annotations
import copy
import json
import re
from dataclasses import dataclass, field, asdict
from typing import Callable

from . import checks, helper, i18n, leads, prompts, saves, schema as sch, timeutil
from .campaign import Campaign, Block, Entry
from .cards import Engine
from .config import Config
from .llm import Backend, LLMError
from .textutil import est_tokens, extract_json
from .tools import REGISTRY
from .turnctx import TurnCtx, ToolError, Hurtable


class TurnError(Exception):
    pass


@dataclass
class TurnResult:
    round: int | None = None
    header: str | None = None
    lines: list[str] = field(default_factory=list)
    status: list[str] = field(default_factory=list)
    narration: str = ""
    gm_delta: str | None = None
    decision: dict | None = None
    save: dict | None = None
    warnings: list[str] = field(default_factory=list)
    ended: bool = False
    blocked: str | None = None
    steps: list[dict] = field(default_factory=list)

    def to_dict(self): return asdict(self)


def hp_line(ctx_or_camp) -> str:
    camp = ctx_or_camp.camp if hasattr(ctx_or_camp, "camp") else ctx_or_camp
    ctx = ctx_or_camp if hasattr(ctx_or_camp, "camp") else TurnCtx(camp)
    p = Hurtable(ctx, "player")
    s = f"HP {p.hp}/{p.max_hp}"
    if p.mp is not None: s += f" · MP {p.mp}/{p.max_mp}"
    prog = (camp.player.get("progression") or {}).get("state")
    if prog: s += f" · level {prog['level']} (XP {prog['xp']})"
    return s + " [host]"


def header(camp: Campaign, n: int) -> str:
    t, lang = camp.time, camp.language
    place = camp.location_name()
    if i18n.is_zh(lang):
        place = i18n.glossary_form(camp.glossary(), str(camp.readable["world_state"]["location"]), place)
    w = i18n.header_words(lang)
    when = timeutil.date_label(t, lang)
    if camp.profile == "lite":
        return f"R {n} | {when} {timeutil.clock_label(t)} | {place} | {w['save']} R{camp.T}"
    return f"{w['round'].format(n=n)} | {when} | {timeutil.clock_label(t)} | {place} | {w['saved']} R{camp.S} · {w['save']} R{camp.T}"


def gm_view(block: Block) -> str:
    if not block.entries:
        return f"GM-Δ {block.round} none"
    out = [f"GM-Δ {block.round} ⟵ {block.prev}"]
    for e in block.entries:
        out.append(f"  {e.op} {e.id} :: " + ("[hidden — kept in the capsule]" if e.hidden else e.content))
    return "\n".join(out)


class Game:
    def __init__(self, cfg: Config, backend: Backend):
        self.cfg, self.backend = cfg, backend
        helper.load(cfg.engine_dir)
        self.engine = Engine(cfg.engine_dir)
        self.system = prompts.referee_system(self.engine)
        self.narr_sys = prompts.narrator_system(self.engine)
        self.check_sys = prompts.checker_system(self.engine)
        need = est_tokens(self.system) + cfg.model.max_new_tokens + 5000
        if backend.n_ctx < need:
            raise TurnError(f"the model context ({backend.n_ctx} tokens) is too small: the engine rules alone need about "
                            f"{need} tokens. Raise n_ctx (or use a model with a longer context). The rules are never cut.")
        self.step_schema = prompts.step_schema_per_tool() if backend.name == "llama_cpp" else prompts.step_schema()

    # ---------------------------------------------------------------------------------------
    def _chat(self, msgs, **kw):
        try:
            return self.backend.chat(msgs, **kw)
        except LLMError as e:
            raise TurnError(str(e))

    def _triage(self, camp, ctx, text) -> dict:
        if leads.needs_guidance(camp, text):                  # recognised in code: a small model must not improvise these
            ctx.guidance = True
            return {"triage": "GUIDANCE", "intent": "the player asks what they can do next", "rows": []}
        brief = prompts.state_brief(camp, hp_line(ctx))
        raw = self._chat([{"role": "system", "content": self.system},
                          {"role": "user", "content": prompts.triage_user(self.engine, camp, text, brief)}],
                         schema=prompts.TRIAGE_SCHEMA, temperature=0.1, max_tokens=300)
        try:
            t = extract_json(raw)
            assert t.get("triage") in ("FAST", "LOOP", "RETRIEVAL", "CONTINUATION")      # GUIDANCE is decided in code only
            t["rows"] = [r for r in t.get("rows", []) if any(r == x.id for x in self.engine.routes)]
        except Exception:
            t = {"triage": "LOOP", "intent": text, "rows": ["r01", "r02"]}
        rows = set(t["rows"])
        if camp.session["combat"]: rows |= {"r04", "r05", "r02"}
        if camp.session.get("pending_odds"): rows.add("r02")
        if camp.numeric and t["triage"] in ("LOOP", "CONTINUATION"): rows.add("r22")
        t["rows"] = sorted(rows)
        return t

    def _cards(self, camp, triage, budget_tokens):
        cards = self.engine.cards_for(triage["rows"], camp.modules)
        keep, used, dropped = [], 0, []
        for c in cards:
            if used + c.tokens <= budget_tokens:
                keep.append(c); used += c.tokens
            else:
                dropped.append(c.ref)
        return keep, dropped

    def _fit(self, msgs, limit):
        def total(): return sum(est_tokens(m["content"]) for m in msgs)
        i = 2
        while total() > limit and i < len(msgs) - 2:
            if msgs[i]["role"] == "user" and msgs[i]["content"].startswith("TOOL RESULT") and len(msgs[i]["content"]) > 160:
                msgs[i] = {"role": "user", "content": msgs[i]["content"][:120] + " … [elided to fit context]"}
            i += 1

    # ---- the referee loop ------------------------------------------------------------------
    def _referee(self, camp, ctx, text, triage, on_event, opening=False):
        budget = self.backend.n_ctx - self.cfg.model.max_new_tokens - est_tokens(self.system) - 2500
        cards, dropped = self._cards(camp, triage, int(budget * 0.5))
        extra = ""
        if triage.get("triage") == "GUIDANCE":
            cards = [self.engine.card_by_ref("13.6")] + cards
            extra = leads.guidance_directive(camp, text, ctx.tree())
        for c in cards: ctx.opened_cards.add(c.ref)
        user = prompts.turn_user(camp, ctx.tree(), text, triage, cards, hp_line(ctx), self.cfg.game.history_turns, opening, extra)
        msgs = [{"role": "system", "content": self.system}, {"role": "user", "content": user}]
        steps, bad = [], 0
        for _ in range(self.cfg.game.max_referee_steps):
            self._fit(msgs, self.backend.n_ctx - self.cfg.model.max_new_tokens - 800)
            raw = self._chat(msgs, schema=self.step_schema, temperature=0.3, max_tokens=1400)
            try:
                obj = extract_json(raw)
                name, args = obj["tool"], obj.get("args") or {}
                tool = REGISTRY[name]
            except Exception:
                bad += 1
                if bad > 3: raise TurnError("the model keeps returning malformed tool calls")
                msgs += [{"role": "assistant", "content": raw[:600]},
                         {"role": "user", "content": "TOOL RESULT: invalid reply. Answer with exactly one JSON object "
                                                     f'{{"tool": <one of {list(REGISTRY)}>, "args": {{...}}}}.'}]
                continue
            errs = sch.validate(args, tool.schema)
            if errs:
                res = "REFUSED: " + "; ".join(errs[:6])
                if name in ("check", "ask"): ctx.check_refused = True
            else:
                try:
                    res = tool.fn(ctx, args)
                    bad = 0
                    if name in ("check", "ask", "resume_check"): ctx.check_refused = False
                except ToolError as e:
                    res = f"REFUSED: {e}"
                    if name in ("check", "ask", "resume_check"): ctx.check_refused = True
                except Exception as e:                       # a bug must not corrupt the turn
                    raise TurnError(f"tool {name} failed: {type(e).__name__}: {e}")
            steps.append({"tool": name, "result": str(res)[:300]})
            on_event({"type": "step", "tool": name, "result": str(res)[:160]})
            msgs += [{"role": "assistant", "content": json.dumps(obj, ensure_ascii=False)},
                     {"role": "user", "content": f"TOOL RESULT ({name}): {res}"}]
            if ctx.closed is not None:
                return steps, dropped
        raise TurnError("the referee did not close the turn in time")

    # ---- narration + audit -----------------------------------------------------------------
    def _narrate(self, camp, ctx, text, closed, on_event):
        lite = camp.profile == "lite"
        visible, dialogue = closed["visible"], closed.get("dialogue") or []
        results = list(ctx.lines) + list(ctx.status)
        decision = closed.get("decision")
        prev = camp.session["history"][-1]["narration"] if camp.session["history"] else ""
        issues, prose, warnings = None, "", []
        for attempt in range(self.cfg.game.narration_retries + 1):
            on_event({"type": "phase", "text": "narrating" if attempt == 0 else f"rewriting (attempt {attempt + 1})"})
            prose = self._chat([{"role": "system", "content": self.narr_sys},
                                {"role": "user", "content": prompts.narrator_user(camp, text, visible, dialogue, results,
                                                                                  ctx.learned, decision, prev, lite, issues, ctx.guidance)}],
                               temperature=0.8, max_tokens=420 if lite else 1100).strip()
            det = checks.check_prose(prose, camp.language, lite, ctx.secret_terms, bool(decision))
            llm_issues = []
            if not det and prose:
                try:
                    raw = self._chat([{"role": "system", "content": self.check_sys},
                                      {"role": "user", "content": prompts.checker_user(camp, text, visible, dialogue, results, prose)}],
                                     schema=prompts.CHECK_SCHEMA, temperature=0.0, max_tokens=500)
                    verdict = extract_json(raw)
                    if not verdict.get("ok", True):
                        llm_issues = [f"{i['kind']}: “{i['quote'][:80]}” — {i['why']}" for i in verdict.get("issues", [])][:5]
                except Exception:
                    llm_issues = []                           # an unavailable checker never blocks play
            issues = det + llm_issues
            if not issues:
                return prose, warnings
        leak = any("secret term" in i for i in issues)
        if leak or not prose:
            warnings.append("narration could not be made safe; showing the plain facts instead")
            prose = " ".join(v.rstrip(".") + "." for v in visible)
        else:
            warnings.append("checker still had concerns: " + " | ".join(issues))
        return prose, warnings

    # ---- the turn ----------------------------------------------------------------------------
    def play(self, camp: Campaign, text: str, on_event: Callable = lambda e: None) -> TurnResult:
        text = text.strip()
        if not text:
            raise TurnError("empty input")
        return self._turn(camp, text, on_event, opening=False)

    def opening(self, camp: Campaign, on_event: Callable = lambda e: None) -> TurnResult:
        return self._turn(camp, "", on_event, opening=True)

    def _turn(self, camp: Campaign, text: str, on_event, opening: bool) -> TurnResult:
        if camp.session.get("ended"):
            raise TurnError("the character is dead. Load an earlier save to continue.")
        if not opening and camp.rnd >= camp.T and camp.session.get("deferral") != "one_round":
            return TurnResult(blocked="save_due", narration="A checkpoint save is due and could not be produced. "
                              "Retry the save, or choose “continue unsaved” (one more round only).")
        snap = camp.snapshot()
        ctx = TurnCtx(camp, text, engine=self.engine)
        ctx.pending_at_start = copy.deepcopy(camp.session.get("pending_odds"))
        try:
            on_event({"type": "phase", "text": "reading the situation"})
            triage = {"triage": "LOOP", "intent": "opening", "rows": []} if opening else self._triage(camp, ctx, text)
            on_event({"type": "phase", "text": f"referee ({triage['triage']})"})
            steps, dropped = self._referee(camp, ctx, text, triage, on_event, opening)
            closed = ctx.closed
            prose, warnings = self._narrate(camp, ctx, text, closed, on_event)
            if dropped:
                warnings.append(f"context was tight; engine sections not shown to the model this turn: {dropped} "
                                "(it can still open them itself)")
        except Exception:
            camp.restore(snap)
            raise
        return self._commit(camp, ctx, text, closed, prose, warnings, steps, on_event, opening)

    def _commit(self, camp, ctx, text, closed, prose, warnings, steps, on_event, opening) -> TurnResult:
        opened = bool(closed["opened_round"]) and not opening
        if ctx.pending_at_start and camp.session.get("pending_odds") == ctx.pending_at_start and not ctx.stopped_for_odds:
            camp.session["pending_odds"] = None             # the player changed or dropped the shown roll
        lang = camp.language
        res = TurnResult(lines=[i18n.localize_line(l, lang) for l in ctx.lines], status=[i18n.localize_status(x, lang) for x in ctx.status], narration=prose, decision=closed.get("decision"),
                         warnings=warnings, steps=steps)
        for L in closed.get("player_learned") or []:
            camp.readable["index"].setdefault(L["section"], {})[L["id"]] = L["line"]
        if closed.get("plan") is not None:
            camp.session["plan"] = closed["plan"]
        if opened:
            n = camp.rnd + 1
            res.round, res.header = n, header(camp, n)
            entries = list(ctx.entries)
            if camp.session.get("clear_deferral"):
                entries.append(Entry("~", "continuity_status.save_deferral", "null", True)); camp.session["clear_deferral"] = False
            block = camp.make_block(n, entries)
            camp.commit_block(block)
            camp.readable["round"]["last_completed_round"] = n
            camp.session["dues"] = []
            res.gm_delta = gm_view(block)
            camp.closed_readable = copy.deepcopy(camp.readable)
            if camp.session.get("deferral") == "one_round":
                camp.session["deferral"] = "spent"          # exactly one more ROUND, then the save comes first
        else:
            camp.pending.extend(ctx.entries)
        camp.session["history"].append({"player": text or "(start)", "narration": prose, "round": res.round,
                                        "header": res.header, "lines": res.lines, "status": res.status})
        res.ended = bool(camp.session.get("ended"))
        camp.write_journal()
        if opened and camp.rnd >= camp.T and camp.session.get("deferral") != "spent":
            res.save = self.save(camp, on_event)
        elif opened and camp.rnd >= camp.T:
            res.save = {"failed": "save still due", "blocked": True}
        return res

    # ---- checkpoint ------------------------------------------------------------------------------
    def save(self, camp: Campaign, on_event: Callable = lambda e: None) -> dict:
        on_event({"type": "phase", "text": "saving (merge + validate)"})
        last = None
        for _ in range(2):                                    # engine §16.3 ON FAIL: retry once
            try:
                r = saves.build_save(camp)
                if camp.session.get("deferral"):
                    camp.session["deferral"] = None; camp.session["clear_deferral"] = True; camp.write_journal()
                return {"path": r["path"], "round": r["round"], "valid": True, "dues": r.get("dues", []),
                        "already": bool(r.get("already"))}
            except saves.SaveFailure as e:
                last = {"failed": str(e), "detail": e.detail}
            except Exception as e:
                last = {"failed": f"{type(e).__name__}: {e}"}
        return last

    def continue_unsaved(self, camp: Campaign):
        """Engine §16.3: only after a real failure; allows exactly one more ROUND."""
        camp.session["deferral"] = "one_round"
        camp.pending.append(Entry("+", "continuity_status.save_deferral", "one_round", True))
        camp.write_journal()


def status_panel(camp: Campaign) -> dict:
    ctx = TurnCtx(camp)
    p = Hurtable(ctx, "player")
    pl = camp.player
    prog = (pl.get("progression") or {}).get("state")
    return {
        "name": pl.get("identity", {}).get("name"), "archetype": pl.get("archetype"), "job": pl.get("job"),
        "hp": p.hp, "max_hp": p.max_hp, "mp": p.mp, "max_mp": p.max_mp,
        "level": prog and prog["level"], "xp": prog and prog["xp"],
        "vitality": pl.get("vitality"),
        "time": f"{timeutil.date_label(camp.time)} {timeutil.clock_label(camp.time)}", "daypart": camp.time.get("daypart"),
        "location": camp.location_name(), "environment": camp.readable["world_state"].get("environment"),
        "money": pl.get("money"), "resources": pl.get("resources"), "equipment": pl.get("equipment"),
        "injuries": pl.get("condition", {}).get("injuries"), "fatigue": pl.get("condition", {}).get("fatigue"),
        "skills": pl.get("skills"), "fighting_style": pl.get("fighting_style"), "knowledge": pl.get("knowledge"),
        "index": camp.readable["index"], "round": camp.rnd, "S": camp.S, "T": camp.T,
        "profile": camp.profile, "language": camp.language, "encoding": camp.encoding,
        "plan": camp.session.get("plan"), "combat": camp.session.get("combat"),
        "pending_odds": bool(camp.session.get("pending_odds")), "ended": bool(camp.session.get("ended")),
        "save_due": camp.rnd >= camp.T, "item_points": pl.get("item_points"),
    }
