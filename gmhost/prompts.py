# Copyright (c) 2026 West132.WL. All rights reserved.
"""Prompt assembly. Engine and AI_RULES text is quoted verbatim by Engine/cards; only the HOST NOTES
and the tool documentation below are written for this software."""
from __future__ import annotations
import copy
import json

import yaml

from . import schema as sch
from .campaign import Campaign
from .cards import Engine, Card
from .textutil import lang_name
from .tools import REGISTRY
from . import timeutil

HOST_NOTES = """\
HOST NOTES — how this software divides the work (the engine above wins any conflict)

You are the referee brain of the engine above, running inside a host program that does everything mechanical:
- The host rolls ALL dice and computes Difficulty, odds, damage, HP/MP maxima, XP, levels, skill evidence, clocks, time and dates.
  You never type or invent a die result, total, HP or XP number. You supply the BOUND INPUTS (capability, challenge, conditions
  with their facts, tool, stakes) and the host returns the results.
- The host prints the engine's own lines (header, roll, damage, answer, odds) and builds the GM-Δ block, the capsule and saves.
  Wherever the engine says "I" do a step, you make that step's JUDGEMENT and call the tool that applies it.
- A fact exists only once written: use `commit` (cause first, I2). Narration never creates facts (I9).
- A separate NARRATOR writes the prose and sees ONLY what you put in close_round `visible`/`dialogue` plus the host's results — never
  hidden state. A separate CHECKER audits the prose against your `visible` list. So `visible` must hold everything the player should
  perceive this turn, in order, and nothing they should not (I5).
- Keep to the engine's loop: TRIAGE → LOAD → READ → GATE → DECIDE → COMMIT → EXECUTE → APPLY → HOOK → RENDER → CHECK → PERSIST. Run only
  the steps whose trigger fired. FAST actions need no roll and no round. Never stop for confirmation during routine continuation.
- Use `lookup` rather than guessing; use `open_cards` when the output touches a section you have not been given (§2.1).
- When a tool refuses, read the reason and fix the call; the refusal is the engine's rule, not an obstacle to argue with.

OUTPUT PROTOCOL: every reply is exactly ONE JSON object {"tool": "<name>", "args": {...}} and nothing else. End every turn with close_round.
"""


def tools_doc() -> str:
    out = ["TOOLS (arguments marked `?` are optional)"]
    for t in REGISTRY.values():
        out.append(f"\n## {t.name}\n{t.doc}\nargs:\n{sch.render(t.schema, 1)}")
    return "\n".join(out)


def referee_system(eng: Engine) -> str:
    return "\n\n".join([
        "ROLE: REFEREE",
        "You are the GM brain of a persistent world simulator. The documents below are your binding rules, quoted verbatim.",
        f"======== NEW ENGINE v{eng.version} — PART 0 (always in force) ========\n{eng.part0_text()}",
        f"======== AI RULES v{eng.version} — §1 and §2 ========\n{eng.rules_section('1')}\n\n{eng.rules_section('2')}",
        f"======== {HOST_NOTES}",
        f"======== {tools_doc()}",
    ])


def strict(schema: dict) -> dict:
    """Closed objects for constrained decoding (free-form `data` objects stay open)."""
    s = copy.deepcopy(schema)
    def walk(n):
        if isinstance(n, dict):
            if n.get("type") == "object" and n.get("properties"):
                n["additionalProperties"] = False
            for v in n.values(): walk(v)
        elif isinstance(n, list):
            for v in n: walk(v)
    walk(s)
    return s


def step_schema() -> dict:
    return {"type": "object", "properties": {
        "tool": {"type": "string", "enum": list(REGISTRY)},
        "args": {"type": "object"}}, "required": ["tool", "args"]}


def step_schema_per_tool() -> dict:
    return {"oneOf": [{"type": "object", "properties": {"tool": {"const": t.name}, "args": strict(t.schema)},
                       "required": ["tool", "args"], "additionalProperties": False} for t in REGISTRY.values()]}


TRIAGE_SCHEMA = {"type": "object", "properties": {
    "triage": {"type": "string", "enum": ["FAST", "LOOP", "RETRIEVAL", "CONTINUATION"]},
    "intent": {"type": "string"},
    "rows": {"type": "array", "items": {"type": "string"}}}, "required": ["triage", "intent", "rows"]}


def triage_user(eng: Engine, camp: Campaign, text: str, brief: str) -> str:
    return (f"TRIAGE (engine §2). Classify this event.\n\nPLAYER SAYS: {text}\n\nSTATE BRIEF:\n{brief}\n\n"
            "FAST = the player's own ordinary action: possible, safe, certain, nobody else affected or watching, nothing lasting.\n"
            "LOOP = someone else affected · uncertain or risky outcome · lasting change.\n"
            "RETRIEVAL = the player only asks what they have/know/see (never advances state).\n"
            "CONTINUATION = established intent/plan/routine carried on under the current order.\n\n"
            f"ROUTING TABLE (engine §2.1) — list the ids of every row that applies to what is about to happen:\n{eng.routing_table()}\n\n"
            'Reply with JSON {"triage": ..., "intent": "<player-owned intent in one sentence>", "rows": ["r01", ...]}.')


# ---- state slice ---------------------------------------------------------------------------
def _yaml(x, cap=1400) -> str:
    t = yaml.safe_dump(x, allow_unicode=True, sort_keys=False, width=120, default_flow_style=None).rstrip()
    return t if len(t) <= cap else t[:cap] + "\n… (cut: use lookup)"


def state_brief(camp: Campaign, hp_line: str) -> str:
    t = camp.time
    return (f"{timeutil.date_label(t)} {timeutil.clock_label(t)} ({t.get('daypart')}) · {camp.location_name()} · "
            f"{hp_line} · plan in force: {camp.session.get('plan') or 'none'}")


def ledger_index(tree: dict) -> str:
    lines = []
    for owner in ("npcs", "factions", "locations", "quests", "active_world_pressures", "rights_obligations",
                  "development_threads", "trackers", "locked_case_truths", "open_suspicions"):
        recs = tree.get(owner) or {}
        if not isinstance(recs, dict) or not recs: continue
        items = []
        for k, v in recs.items():
            nm = (v.get("name") or v.get("objective") or v.get("direction") or "") if isinstance(v, dict) else ""
            items.append(f"{k}" + (f" ({str(nm)[:40]})" if nm else ""))
        lines.append(f"{owner}: " + ", ".join(items))
    return "\n".join(lines) or "(no records)"


def state_text(camp: Campaign, tree: dict, hp_line: str, here_cap: int = 5000) -> str:
    rd = camp.readable
    pl = copy.deepcopy(rd["player"])
    pl.get("condition", {}).pop("hp", None); pl.get("condition", {}).pop("mp", None)
    loc_id = rd["world_state"]["location"]
    loc = (tree.get("locations") or {}).get(loc_id)
    if not isinstance(loc, dict):
        loc = None                      # a location recorded as plain text still works; it just has no structure to show
    here = {}
    for k, v in (tree.get("npcs") or {}).items():
        pos = str(((v or {}).get("state") or {}).get("position", "")) if isinstance(v, dict) else ""
        if pos and (pos == loc_id or pos == (loc or {}).get("name")):
            here[k] = v
    q = {k: v for k, v in (tree.get("quests") or {}).items() if isinstance(v, dict) and v.get("status") in ("active", "available", "blocked")}
    parts = [
        f"== TIME / PLACE ==\n{timeutil.date_label(camp.time)} {timeutil.clock_label(camp.time)} ({camp.time.get('daypart')}), season {camp.time.get('season') or '?'}; "
        f"day_index {camp.time['day_index']}; location `{loc_id}`\nenvironment: {json.dumps(rd['world_state'].get('environment'), ensure_ascii=False)}"
        f"\nlocation record: {_yaml(loc, 900) if loc else '(none committed)'}",
        f"== PLAYER ==\n{hp_line}\n{_yaml(pl, 2600)}",
        f"== ORDERS / PLAN IN FORCE ==\n{camp.session.get('plan') or '(none)'}",
    ]
    if camp.session.get("pending_odds"):
        parts.append("== PENDING ODDS-STOP ==\nThe player was shown the odds for: " + camp.session["pending_odds"]["args"]["action"] +
                     "\nIf they confirm (go/yes/roll), call the resume_check tool. If they change or drop it, do NOT resume; treat their new words normally.")
    if camp.session.get("combat"):
        parts.append("== COMBAT (host-tracked) ==\n" + "\n".join(
            f"{k}: {c['name']} [{c['side']}] HP {c['hp']}/{c['max_hp']}, attacks left this exchange {c.get('attacks_left', c.get('attacks', 1))}/{c.get('attacks', 1)}"
            for k, c in camp.session["combat"].items()))
    if camp.session.get("dues"):
        parts.append("== OPEN DUES FROM THE LAST SAVE VALIDATION (fire, replan, or close each in this APPLY — engine §16.3) ==\n- " +
                     "\n- ".join(camp.session["dues"][:12]))
    if int(rd["player"]["condition"].get("hp", 1)) <= 0:
        parts.append("== PLAYER IS DOWN (0 HP) ==\nIncapacitated; further damage kills. The player cannot act until treated (heal) — a helpless actor can be killed "
                     "without a roll. Untreated for 1 hour of world time → roll kind=down_check (11+ wakes at 1 HP, else dies).")
    parts.append(f"== LEDGER INDEX (what exists; use lookup for detail) ==\n{ledger_index(tree)}")
    if here:
        parts.append("== ACTORS HERE ==\n" + "\n".join(f"{k}: {_yaml(v, 1100)}" for k, v in list(here.items())[:6]))
    if q:
        parts.append("== OPEN QUESTS ==\n" + _yaml(q, 1200))
    g = camp.glossary()
    if g:
        parts.append("== GLOSSARY (" + camp.language + ") ==\n" + _yaml(g, 800))
    return "\n\n".join(parts)


def recent_text(camp: Campaign, n: int) -> str:
    h = camp.session["history"][-n:]
    if not h: return "(this is the start)"
    return "\n".join(f"[R{x.get('round') or '–'}] PLAYER: {x['player']}\n    SCENE: {x['narration'][:700]}" for x in h)


def turn_user(camp: Campaign, tree: dict, text: str, triage: dict, cards: list[Card], hp_line: str, history_n: int,
              opening: bool = False) -> str:
    cards_txt = "\n\n".join(f"=== ENGINE §{c.ref} {c.title} (verbatim) ===\n{c.text}" for c in cards) or "(no extra sections routed)"
    head = ("NEW GAME — engine §16.2. Establish the opening situation. There is no ROUND yet: call close_round with opened_round=false and "
            "`visible` = what the player perceives at the start (place, time, who/what is naturally noticeable, their starting activity). "
            "Commit nothing unless the engine requires it; invent nothing (I3)." if opening else
            f"PLAYER SAYS: {text}\nTRIAGE: {triage.get('triage')} — intent: {triage.get('intent')}")
    return (f"{head}\n\n{state_text(camp, tree, hp_line)}\n\n== RECENT PLAY (visible prose, for continuity) ==\n{recent_text(camp, history_n)}"
            f"\n\nENGINE SECTIONS ROUTED FOR THIS TURN (verbatim):\n{cards_txt}\n\n"
            "Respond with ONE tool call as JSON. When the turn is resolved, call close_round.")


# ---- narrator ----------------------------------------------------------------------------------
def narrator_system(eng: Engine) -> str:
    return "\n\n".join([
        "ROLE: NARRATOR",
        "You write the player-visible prose of one turn of a text RPG. You are NOT the referee: you know only the facts you are given.",
        f"======== ENGINE §9 NARRATION (verbatim) ========\n{eng.section_text('9')}",
        f"======== AI RULES — {eng.rules_block('Language')}",
        f"======== AI RULES — {eng.rules_block('Narration craft')}",
        "======== HOST RULES ========\n"
        "- Narrate ONLY the facts under WHAT THE PLAYER PERCEIVES, in order. Add sensory texture, never new facts: no new objects, people, "
        "motives, causes, numbers or outcomes (I3, I9).\n"
        "- Never reveal or hint at anything not listed. Never decide, say or feel anything for the player character beyond what is listed (I4).\n"
        "- Dice, totals, HP and XP are shown to the player by the host; do not print them. Wounds, fatigue and danger may be described in words.\n"
        "- Spoken lines: write each NPC in their own voice from the gist given; keep the meaning.\n"
        "- If a DECISION is given, end by putting that choice to the player in-world; list the options plainly.\n"
        "- Write natively in the game language. Output only the prose — no headings, no markdown fences, no notes."])


def narrator_user(camp: Campaign, text: str, visible: list[str], dialogue: list[dict], results: list[str],
                  learned: list[str], decision: dict | None, prev: str, lite: bool, retry_issues: list[str] | None) -> str:
    th = camp.readable["narrative_theme"]["current"]
    p = camp.player
    parts = [
        f"GAME LANGUAGE: {lang_name(camp.language)}",
        f"LENGTH: " + ("at most ~120 words unless a real decision, fight or reveal needs more" if lite else "as long as the material change deserves; compress routine"),
        f"THEME (style only): tone {th.get('tone')}; style {th.get('style')}",
        f"PLAYER CHARACTER: {p.get('identity', {}).get('name')} — {p.get('archetype', '')}",
        f"SCENE: {timeutil.date_label(camp.time)} {timeutil.clock_label(camp.time)}, {camp.location_name()}",
        f"PLAYER'S WORDS: {text}" if text else "OPENING OF THE GAME (no player action yet)",
        "WHAT THE PLAYER PERCEIVES (narrate exactly these, in order):\n" + "\n".join(f"- {v}" for v in visible),
    ]
    if dialogue:
        parts.append("SPOKEN LINES (gist; voice them):\n" + "\n".join(f"- {d['who']}: {d['gist']}" + (f" ({d['tone']})" if d.get('tone') else "") for d in dialogue))
    if results:
        parts.append("ENGINE RESULTS (already shown to the player above your prose; describe in words only):\n" + "\n".join(f"- {r}" for r in results))
    if learned:
        parts.append("QUIET CHANGES to mention lightly:\n" + "\n".join(f"- {r}" for r in learned))
    if decision:
        parts.append(f"DECISION TO PUT TO THE PLAYER: {decision['question']}\nOptions: " + " | ".join(decision["options"]))
    g = camp.glossary()
    if g: parts.append("GLOSSARY (use these forms exactly): " + json.dumps(g, ensure_ascii=False))
    if prev: parts.append("PREVIOUS PROSE (continuity only; do not repeat):\n" + prev[-900:])
    if retry_issues:
        parts.append("YOUR LAST DRAFT WAS REJECTED. Fix exactly this and write again:\n" + "\n".join(f"- {i}" for i in retry_issues))
    parts.append("Write the prose now.")
    return "\n\n".join(parts)


# ---- checker -------------------------------------------------------------------------------------
CHECK_SCHEMA = {"type": "object", "properties": {
    "ok": {"type": "boolean"},
    "issues": {"type": "array", "items": {"type": "object", "properties": {
        "kind": {"type": "string", "enum": ["new_fact", "reveal", "agency", "order_violation", "numbers", "language", "other"]},
        "quote": {"type": "string"}, "why": {"type": "string"}}, "required": ["kind", "quote", "why"]}}},
    "required": ["ok", "issues"]}


def checker_system(eng: Engine) -> str:
    return "\n\n".join([
        "ROLE: CHECKER",
        "You audit one passage of narration for a text RPG against the facts the narrator was given. Be strict but literal: flag only real violations.",
        f"======== ENGINE §5 INVARIANTS (verbatim) ========\n{eng.section_text('5')}",
        f"======== ENGINE §9 NARRATION (verbatim) ========\n{eng.section_text('9')}",
        f"======== AI RULES — {eng.rules_block('Invariant failures seen')}",
        "======== WHAT TO FLAG ========\n"
        "new_fact: prose asserts a person, object, cause, motive, outcome, number or event that is not in the given facts.\n"
        "reveal: prose exposes or hints at something the player has not perceived (I5, I9).\n"
        "agency: prose decides, says, feels or does something for the player character that the player did not choose (I4), or lets an ally obey merely because they are an ally.\n"
        "order_violation: the player's literal words are not honoured (e.g. 'one by one' collapsed, 'from range' broken).\n"
        "numbers: dice, totals, HP or XP are printed in the prose.\n"
        "language: the passage is not in the game language.\n"
        "Atmosphere, rhythm, metaphor and sensory detail that add no fact are fine. Reply as JSON {\"ok\": bool, \"issues\": [...]}; ok=true means no issues."])


def checker_user(camp: Campaign, text: str, visible: list[str], dialogue: list[dict], results: list[str], prose: str) -> str:
    return (f"GAME LANGUAGE: {lang_name(camp.language)}\nPLAYER'S WORDS: {text or '(opening)'}\n\nFACTS THE NARRATOR WAS GIVEN:\n" +
            "\n".join(f"- {v}" for v in visible) +
            ("\nSPOKEN LINES:\n" + "\n".join(f"- {d['who']}: {d['gist']}" for d in dialogue) if dialogue else "") +
            ("\nENGINE RESULTS (host-shown):\n" + "\n".join(f"- {r}" for r in results) if results else "") +
            f"\n\nPASSAGE TO AUDIT:\n\"\"\"\n{prose}\n\"\"\"\n\nAudit it.")
