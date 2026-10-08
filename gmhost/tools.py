# Copyright (c) 2026 West132.WL. All rights reserved.
"""The referee's tools. The model judges; every number, roll and write happens here.

Each tool validates its arguments against the engine's rules and either performs the
change exactly once or refuses with a message the model can act on. Engine lines that
reach the player (rolls, damage, answers) are the helper's own `--brief` output.
"""
from __future__ import annotations
import json
import re
from dataclasses import dataclass
from typing import Callable

import yaml

from . import helper, rules, timeutil
from .campaign import CAPSULE_OWNERS, INDEX_SECTIONS, Entry
from .turnctx import TurnCtx, ToolError, Hurtable

# ---- schema builders -------------------------------------------------------------------
def S(desc="", **kw): return {"type": "string", "description": desc, **kw}
def I(desc="", lo=None, hi=None):
    d = {"type": "integer", "description": desc}
    if lo is not None: d["minimum"] = lo
    if hi is not None: d["maximum"] = hi
    return d
def B(desc=""): return {"type": "boolean", "description": desc}
def E(*vals, desc=""): return {"type": "string", "enum": list(vals), "description": desc}
def A(item, desc="", **kw): return {"type": "array", "items": item, "description": desc, **kw}
def O(props=None, required=(), desc="", extra=True):
    return {"type": "object", "properties": props or {}, "required": list(required), "description": desc}


@dataclass
class Tool:
    name: str
    doc: str
    schema: dict
    fn: Callable


REGISTRY: dict[str, Tool] = {}


def tool(name, doc, schema):
    def deco(fn):
        REGISTRY[name] = Tool(name, doc, schema, fn)
        return fn
    return deco


M = helper.mod  # resolved lazily
_BRIEF_OUT = re.compile(r"Outcome: (Success|Failure)")
_LITE_OUT = re.compile(r"→ (Success|Failure)\s*$")
_DMG = re.compile(r"HP (\d+) → (\d+)(?: — (down|dead))?")
_BAND = re.compile(r"→ (YES, AND|YES|NO, BUT|NO, AND)\s*$")


def _lite(ctx) -> bool:
    return ctx.camp.profile == "lite"


# =========================================================================================
@tool("lookup", "Read a slice of the Ledger (BACKGROUND records overlaid with the capsule). "
      "Use it instead of guessing: e.g. path `npcs.oda_brandt`, `quests`, `active_world_pressures.brine_winds`.",
      O({"path": S("dotted path under npcs, factions, locations, quests, rights_obligations, active_world_pressures, "
                   "locked_case_truths, world_state, ...", minLength=3)}, ["path"]))
def t_lookup(ctx: TurnCtx, a):
    node = ctx.get(a["path"])
    if node is None:
        raise ToolError(f"nothing at {a['path']!r} (it does not exist, so it cannot influence anything: I3)")
    if isinstance(node, dict) and a["path"].count(".") == 0:
        node = {k: (v.get("name") if isinstance(v, dict) and v.get("name") else "…") for k, v in node.items()}
    text = yaml.safe_dump(node, allow_unicode=True, sort_keys=False, width=110) if not isinstance(node, str) else node
    return text if len(text) < 6000 else text[:6000] + "\n… (cut; look up a deeper path)"


@tool("open_cards", "Load more verbatim engine sections (engine §2.1 says which section to open for what). "
      "Refs like `10.3`, `12`, `13.5`, `14.2`, `A`.", O({"refs": A(S(), minItems=1, maxItems=4)}, ["refs"]))
def t_open_cards(ctx: TurnCtx, a):
    eng = ctx.engine
    out = []
    for ref in a["refs"]:
        if ref in ctx.opened_cards:
            out.append(f"[§{ref} is already open above]"); continue
        try:
            card = eng.card_by_ref(ref)
        except KeyError:
            raise ToolError(f"no engine section {ref!r}")
        ctx.opened_cards.add(ref)
        out.append(f"=== ENGINE §{card.ref} (verbatim) ===\n{card.text}")
    return "\n\n".join(out)


# =========================================================================================
_COND = O({"category": E(*rules.CONDITION_CATS), "value": {"type": "integer", "enum": [-1, 1, 2]},
           "fact": S("the concrete state fact that independently changes execution (counted nowhere else)", minLength=8)},
          ["category", "value", "fact"])
_CHECK = O({
    "actor": S("who rolls: `player` (default) or a registered combatant / recorded npc id"),
    "action": S("the attempted action, short", minLength=3),
    "why_uncertain": S("why this could honestly go either way (if an obvious answer exists, do not roll)", minLength=8),
    "capability": O({"mode": E("numeric", "absolute"),
                     "cmp": I("numeric: actor capability (level + skill tier bonus); omit for the player when skill_id is given — the host computes it", 1),
                     "skill_id": S("numeric, player: the skill bound as exercised; the host computes cmp = level + tier bonus"),
                     "gear_item_id": S("module B: the equipment item whose tier boost applies (never also a ToolMod, I8)"),
                     "challenge": I("numeric: the task/opponent's committed Challenge", 1),
                     "capmod": {"type": "integer", "enum": [-4, -2, 0, 2, 4], "description": "absolute: capability band"},
                     "base": I("absolute: the task's own difficulty 1-20", 1, 20),
                     "basis": S("short Difficulty basis, e.g. 'dim light, ordinary lock'")}, ["mode"]),
    "conditions": A(_COND, "execution conditions, one per category, each with its fact (engine §10.3)"),
    "tool": O({"fit": I("-2..+2", -2, 2), "condition": {"type": "integer", "enum": [0, -1, -2]},
               "source": S("what the nonzero ToolMod comes from")}),
    "stakes": O({"cost": E("setback", "loss", "severe"), "cost_text": S("what failure costs, concretely", minLength=5),
                 "reach": E("partial", "full", "decisive"), "reach_text": S("what success achieves", minLength=5),
                 "harm": B("true if the failure cost is HP damage from an attacker/hazard that can reach the actor")},
                ["cost", "cost_text", "reach", "reach_text"]),
    "harm": O({"source_id": S("registered attacker id (combat add), or omit for a hazard"),
               "hazard": E("light", "serious", "grave"),
               "engaged_ids": A(S(), "every engaged attacker (for a severe cost)")}),
    "attack": O({"kind": E("weapon", "power"), "size": S("unarmed|light|one_handed|two_handed|bow  or  T1..T4"),
                 "item_id": S("equipment item used")}, desc="the roller's damage source, for a hit on success"),
    "target_id": S("engaged registered opponent a successful full/decisive roll hits"),
    "context": O({"in_combat": B(), "player_chosen_roll": B("false when the roll comes from the world, not the player's choice"),
                  "covered_by_order": B("true if the player's order/plan/fighting_style already commits to this risk"),
                  "character_can_judge": B(), "hidden_fact_difficulty": B("difficulty rests on a hidden fact")}),
    "skills_exercised": A(S(), "player skill ids bound as exercised"),
    "label": S("roll-line label for a roll that is not the player's"),
}, ["action", "why_uncertain", "capability", "stakes"])


@tool("check", "ONE engine roll (§10.3): 2d10 + CapabilityMod + ToolMod vs Difficulty. You supply the BOUND inputs and stakes; "
      "the host computes Difficulty, rolls, prints the roll line, applies damage/HP from the stakes (§10.4-10.5) and credits skill evidence (§11). "
      "Never call it for a deterministic or impossible action.", _CHECK)
def t_check(ctx: TurnCtx, a):
    camp, sess, m = ctx.camp, ctx.camp.session, M()
    resumed = False
    if a.get("resume"):                                  # reached through the resume_check tool
        po = sess.get("pending_odds")
        if not po:
            raise ToolError("there is no pending odds-stop to resume")
        a, sess["pending_odds"], resumed = po["args"], None, True      # bound context is immutable (I10)
    for need in ("action", "why_uncertain", "capability", "stakes"):
        if need not in a:
            raise ToolError(f"missing {need!r}")
    actor_id = a.get("actor") or "player"
    errs = []
    cap = a["capability"]
    numeric = cap["mode"] == "numeric"
    if numeric:
        if "challenge" not in cap: errs.append("numeric mode needs capability.challenge")
        if "cmp" not in cap and not (actor_id == "player" and cap.get("skill_id")): errs.append("numeric mode needs capability.cmp (or skill_id for the player)")
        if "capmod" in cap or "base" in cap: errs.append("numeric mode: task power lives in the Challenge; drop capmod/base (base is always 10)")
        if not camp.numeric and actor_id == "player": errs.append("numeric_level_xp is not enabled: use mode `absolute`")
    else:
        if "capmod" not in cap or "base" not in cap: errs.append("absolute mode needs capability.capmod and capability.base")
    seen = set()
    cats = {c: 0 for c in rules.CONDITION_CATS}
    for c in a.get("conditions") or []:
        if c["category"] in seen: errs.append(f"category {c['category']} counted twice (I8)")
        seen.add(c["category"]); cats[c["category"]] = c["value"]
    t = a.get("tool") or {}
    fit, cond = int(t.get("fit", 0)), int(t.get("condition", 0))
    if (fit or cond) and not t.get("source"): errs.append("a nonzero ToolMod needs tool.source")
    st = a["stakes"]
    if st.get("harm") and st["cost"] == "setback": errs.append("a setback costs no HP: set harm=false or raise the cost to loss/severe")
    skills = a.get("skills_exercised") or []
    for s in skills:
        if actor_id == "player" and s not in camp.player.get("skills", {}): errs.append(f"player has no skill {s!r}")
    harm = a.get("harm") or {}
    attackers: list[str] = []
    if st.get("harm") and st["cost"] in ("loss", "severe"):
        if not (harm.get("source_id") or harm.get("hazard") or harm.get("engaged_ids")):
            errs.append("harm=true needs harm.source_id, harm.engaged_ids or harm.hazard (§10.4 REACH: an attacker/hazard must be able to reach the actor)")
        attackers = list(harm.get("engaged_ids") or ([harm["source_id"]] if harm.get("source_id") else []))
        for x in attackers:
            if x not in sess["combat"]: errs.append(f"attacker {x!r} is not registered: `combat add` it first")
    cmp_host, boost_note = None, ""
    if numeric and not errs:
        cmp_host = int(cap["cmp"]) if "cmp" in cap else None
        if actor_id == "player" and cap.get("skill_id"):
            sk = camp.player.get("skills", {}).get(cap["skill_id"])
            lvl = ((camp.player.get("progression") or {}).get("state") or {}).get("level")
            if sk is None: errs.append(f"player has no skill {cap['skill_id']!r}")
            elif not lvl: errs.append("no overall level to build capability from; use mode absolute")
            else:
                cmp_host = int(lvl) + rules.TIER_BONUS[sk["tier"]]
                if cap["skill_id"] not in skills: skills = skills + [cap["skill_id"]]
        if cap.get("gear_item_id") and not errs:
            if not camp.modules.get("equipment_power_tiers"): errs.append("equipment_power_tiers is not enabled: no gear boost exists")
            elif fit or cond: errs.append("a gear boost is never also a ToolMod (I8): set tool.fit and tool.condition to 0")
            else:
                it = next((x for x in camp.player.get("equipment", []) if x.get("item_id") == cap["gear_item_id"]), None)
                if it is None or it.get("tier") not in rules.GEAR_BOOST: errs.append(f"no tiered equipment item {cap['gear_item_id']!r}")
                elif it.get("condition") == "critical": errs.append("a critical item gives no boost")
                else:
                    cmp_host += rules.GEAR_BOOST[it["tier"]]
                    boost_note = f" (+{rules.GEAR_BOOST[it['tier']]} from {it['name']})"
    if errs:
        raise ToolError("; ".join(errs))
    kw = dict(fit=fit, condition=cond, **cats)
    if numeric: kw.update(cmp=int(cmp_host), challenge=int(cap["challenge"]))
    else: kw.update(capmod=int(cap["capmod"]), base=int(cap["base"]))
    try:
        odds = m.do_check(helper.check_ns(**kw, odds=True))
    except m.InputError as e:
        raise ToolError(str(e))
    flags = a.get("context") or {}
    in_combat = bool(flags.get("in_combat")) or bool(sess["combat"])
    if (not resumed and actor_id == "player" and not in_combat and flags.get("player_chosen_roll", True)
            and flags.get("character_can_judge", True) and not flags.get("covered_by_order", False)
            and (st["cost"] == "severe" or odds["odds_percent"] < 25)):
        if flags.get("hidden_fact_difficulty"):
            line = f"{a['action']} — the odds can't be judged from here · on failure: {st['cost_text']}"
        else:
            line = m.do_check(helper.check_ns(**kw, odds=True, brief=True, label=a["action"], on_failure=st["cost_text"]))
        ctx.lines.append(line)
        sess["pending_odds"] = {"args": a}
        ctx.stopped_for_odds = True
        return ("ODDS STOP (§10.4): the odds line is shown to the player. Do NOT roll. Now call close_round with "
                "opened_round=false, `visible` declaring the situation and risk in-world, and a `decision` offering "
                "go / change / drop. The roll stays bound exactly as shown.")
    # a new exchange: foes' attack budgets refill (§12 ATTACK BUDGET)
    if in_combat:
        for c in sess["combat"].values():
            if c.get("side", "foe") == "foe": c["attacks_left"] = c.get("attacks", 1)
    label = a.get("label") or (None if actor_id == "player" else Hurtable(ctx, actor_id).name)
    line = m.do_check(helper.check_ns(**kw, brief=not _lite(ctx), lite=_lite(ctx), label=label, basis=cap.get("basis"),
                                      stakes=f"{st['cost']}/{st['reach']}", tool_source=t.get("source")))
    ctx.lines.append(line)
    ctx.rolled = True
    success = bool(_BRIEF_OUT.search(line) and _BRIEF_OUT.search(line).group(1) == "Success") if not _lite(ctx) \
        else bool(_LITE_OUT.search(line) and _LITE_OUT.search(line).group(1) == "Success")
    difficulty = int(re.search(r"Difficulty: (\d+)" if not _lite(ctx) else r"vs (\d+)", line).group(1))
    effects = _apply_stakes(ctx, a, success, actor_id, attackers)
    if success and actor_id == "player":
        effects += _accrue(ctx, a, difficulty, skills)
    return (f"Outcome: {'SUCCESS' if success else 'FAILURE'} ({st['reach'] if success else st['cost']}). "
            "Bound stakes applied by the host:\n- " + "\n- ".join(effects or ["no HP change"]) +
            "\nNow narrate nothing yet: commit the consequences this outcome causes (tools), or close_round. "
            "A failure stays a failure (I11); success-partial is not failure.")


def hit(ctx: TurnCtx, target: Hurtable, kind: str, size: str, soak: int, hits: int, who: str | None = None) -> tuple[str, str | None]:
    """Apply `hits` damage hits via the helper. Returns (effect text, state)."""
    m = M()
    dice = rules.damage_dice(kind, size)
    line = m.do_harm(helper.ns(hp=target.hp, max=target.max_hp, dice=dice, amount=None, soak=soak, hits=hits,
                               brief=True, who=target.name))
    first, _, rest = line.partition("\n")
    ctx.lines.append(first)
    mt = _DMG.search(first)
    before, after, state = int(mt.group(1)), int(mt.group(2)), mt.group(3)
    target.set_hp(after)
    text = f"{target.name} HP {before} → {after}" + (f" [{state}]" if state else "")
    ctx.status.append(f"{target.name}: HP {before} → {after}/{target.max_hp}" + (f" — {state}" if state else ""))
    if rest and target.kind == "combat":
        ctx.log.append(f"{target.name} took a hit ≥ ½ max HP; incidental combatants carry no lasting injuries")
    elif rest:
        ctx.must_settle[f"injury:{target.id}"] = (
            f"{target.name} suffers a LASTING INJURY (§10.5): add {{injury, home, effect}} "
            + ("with player_update kind=injury_add" if target.kind == "player" else f"with commit `~ npcs.{target.id}.state.injuries`"))
        text += " + lasting injury to record"
    if state == "dead" and target.kind == "player":
        ctx.camp.session["ended"] = True
        ctx.camp.player["status"] = "dead"
    return text, state


def _apply_stakes(ctx: TurnCtx, a: dict, success: bool, actor_id: str, attackers: list[str]) -> list[str]:
    st, out, sess = a["stakes"], [], ctx.camp.session
    actor = Hurtable(ctx, actor_id)
    if success:
        out.append(f"success reach = {st['reach']}: {st['reach_text']}")
        if st["reach"] in ("full", "decisive") and a.get("target_id") and a.get("attack"):
            tgt = Hurtable(ctx, a["target_id"])
            at = a["attack"]
            kind = "weapon" if at["kind"] == "weapon" else "power"
            try:
                txt, state = hit(ctx, tgt, kind, at["size"], tgt.soak, 1)
            except ValueError as e:
                raise ToolError(str(e))
            out.append("one hit on the engaged opponent: " + txt)
        return out
    out.append(f"failure cost = {st['cost']}: {st['cost_text']}")
    if st["cost"] == "setback" or not st.get("harm"):
        return out
    h = a.get("harm") or {}
    if attackers:
        live = [x for x in attackers if sess["combat"][x].get("attacks_left", 1) > 0 and sess["combat"][x]["hp"] > 0]
        if not live:
            out.append("every attacker is out of attacks or down: no harm — the failure is a setback (I8)")
            return out
        severe_all = st["cost"] == "severe"
        if severe_all and len(attackers) >= 2:
            for x in live:
                c = sess["combat"][x]
                txt, _ = hit(ctx, actor, c["damage"]["kind"], c["damage"]["size"], actor.soak, 1)
                c["attacks_left"] = 0
                out.append(f"{c['name']} hits: {txt}")
        else:
            x = live[0]; c = sess["combat"][x]
            n = 2 if severe_all else 1
            txt, _ = hit(ctx, actor, c["damage"]["kind"], c["damage"]["size"], actor.soak, n)
            c["attacks_left"] = 0 if severe_all else c.get("attacks_left", 1) - 1
            out.append(f"{c['name']} hits{' twice' if n == 2 else ''}: {txt}")
    else:
        n = 2 if st["cost"] == "severe" else 1
        txt, _ = hit(ctx, actor, "hazard", h.get("hazard", "light"), actor.soak, n)
        out.append(f"hazard hits{' twice' if n == 2 else ''}: {txt}")
    return out


def _accrue(ctx: TurnCtx, a: dict, difficulty: int, skills: list[str]) -> list[str]:
    camp, m, out = ctx.camp, M(), []
    gp = camp.player.setdefault("growth_period", {"opened": camp.time["day_index"], "credited": []})
    cap = a["capability"]
    level = ((camp.player.get("progression") or {}).get("state") or {}).get("level") if camp.numeric else None
    for sid in dict.fromkeys(skills):
        if sid in gp["credited"]:
            ctx.log.append(f"{sid}: already credited this growth period"); continue
        sk = camp.player["skills"][sid]
        psl = rules.personal_skill_level(level, sk["tier"]) if (cap["mode"] == "numeric" and level) else None
        r = m.do_accrue(helper.ns(cls=sk["class"], tier=sk["tier"],
                                  challenge=cap.get("challenge") if cap["mode"] == "numeric" else None,
                                  personal_skill_level=psl, difficulty=difficulty, success=True))
        if r["evidence_gain"] <= 0:
            continue
        field = r["add_to"]
        sk[field] = int(sk.get(field, 0)) + r["evidence_gain"]
        gp["credited"].append(sid)
        ctx.log.append(f"evidence: {sid} +{r['evidence_gain']} → {field} {sk[field]}")
        out.append(f"skill evidence credited ({sid} +{r['evidence_gain']}); tier changes only at a growth boundary")
    return out


# =========================================================================================
@tool("resume_check", "Roll the pending odds-stop check EXACTLY as it was shown to the player (bound context is immutable, I10). "
      "Only when the player confirmed (go / yes / roll). No arguments.", O())
def t_resume_check(ctx: TurnCtx, a):
    return t_check(ctx, {"resume": True})


@tool("ask", "An OPEN QUESTION (§13.1): 2d10 + likelihood (each point one recorded fact, max 2 per column). "
      "Only when the record does not settle it and the outcome could honestly flip. Settled → decide, do not roll.",
      O({"question": S("one yes/no question", minLength=8),
         "settle_test": S("the obvious answer if the record settled it, and why the record does NOT settle it", minLength=12),
         "label": S("who or what answers", minLength=2),
         "likelihood": I("-3..+3", -3, 3),
         "for": A(S(), maxItems=2), "against": A(S(), maxItems=2)},
        ["question", "settle_test", "label", "likelihood"]))
def t_ask(ctx: TurnCtx, a):
    lk, fo, ag = a["likelihood"], a.get("for") or [], a.get("against") or []
    for fact in fo + ag:
        if len(fact.split()) < 3 or len(fact) < 15:
            raise ToolError(f"each likelihood fact must be a recorded fact written as a sentence (who/what/why), not a keyword: {fact!r}")
    if lk > 0 and not fo: raise ToolError("positive likelihood needs at least one recorded fact in `for`")
    if lk < 0 and not ag: raise ToolError("negative likelihood needs at least one recorded fact in `against`")
    if abs(lk) > len(fo) + len(ag) + (1 if lk == 0 else 0) and abs(lk) > 0 and abs(lk) > len(fo) + len(ag):
        raise ToolError("each likelihood point must be one recorded fact")
    try:
        line = M().do_ask(helper.ns(likelihood=lk, for_="; ".join(fo) or None, against="; ".join(ag) or None,
                                    label=a["label"], brief=not _lite(ctx), lite=_lite(ctx)))
    except M().InputError as e:
        raise ToolError(str(e))
    ctx.lines.append(line)
    ctx.rolled = True
    band = _BAND.search(line).group(1)
    return (f"Answer: {band}. The band is the answer; narration never moves it. YES,AND = more than asked within means "
            "and authority · YES = as asked · NO,BUT = partly (less/later/on their terms; never a smaller free gift) · "
            "NO,AND = refused + the smallest proportionate trouble from this actor, never aimed at the player's secrets (I6). "
            "Commit what this answer changes.")


# =========================================================================================
@tool("combat", "Register or clear combatants for this fight (interaction state; persistent actors live in the ledger). "
      "Opponent max HP, damage dice and attack budget come from the engine tables.",
      O({"action": E("add", "remove", "clear"),
         "id": S("short stable id, e.g. wolf1"), "name": S(),
         "side": E("foe", "ally"), "size": E(*rules.SIZES), "v": I("overall level / vitality value V (§10.5)", 1, 40),
         "damage_kind": E("weapon", "creature", "hazard", "power"),
         "damage_size": S("unarmed|light|one_handed|two_handed|bow | small|man_sized|large|huge | T1..T4"),
         "soak": E("none", "light", "heavy"),
         "attacks": I("independent attacks per exchange (man-sized fighter 1; dragon 2)", 1, 4)}, ["action"]))
def t_combat(ctx: TurnCtx, a):
    combat = ctx.camp.session["combat"]
    if a["action"] == "clear":
        combat.clear(); ctx.camp.session["plan"] = ""
        return "combat cleared"
    if "id" not in a: raise ToolError("`id` required")
    if a["action"] == "remove":
        combat.pop(a["id"], None); return f"{a['id']} removed"
    for k in ("name", "v", "damage_kind", "damage_size"):
        if k not in a: raise ToolError(f"adding a combatant needs {k!r}")
    try:
        dice = rules.damage_dice(a["damage_kind"], a["damage_size"])
    except ValueError as e:
        raise ToolError(str(e))
    mx = rules.max_vitals(a["v"], a.get("size", "normal"))["max_hp"]
    combat[a["id"]] = {"name": a["name"], "side": a.get("side", "foe"), "max_hp": mx, "hp": mx,
                       "damage": {"kind": a["damage_kind"], "size": a["damage_size"]},
                       "soak": rules.SOAK[a.get("soak", "none")], "attacks": a.get("attacks", 1),
                       "attacks_left": a.get("attacks", 1)}
    return f"{a['name']} registered: max HP {mx}, damage {dice}, soak {rules.SOAK[a.get('soak','none')]}, {a.get('attacks',1)} attack(s)/exchange"


@tool("damage", "Harm outside a player roll: a hazard, or an attacker hitting an ALLY/bystander (its own resolution). "
      "Dice come from the §10.5 tables; HP, down and death are computed by the host.",
      O({"target_id": S(), "kind": E("weapon", "creature", "hazard", "power"), "size": S(), "hits": I("", 1, 6),
         "source_id": S("registered attacker (spends one of its attacks this exchange)"),
         "reason": S("why this harm happens", minLength=5)}, ["target_id", "kind", "size", "reason"]))
def t_damage(ctx: TurnCtx, a):
    sess = ctx.camp.session
    if a.get("source_id"):
        c = sess["combat"].get(a["source_id"])
        if not c: raise ToolError(f"{a['source_id']!r} is not registered")
        if c.get("attacks_left", 1) <= 0:
            raise ToolError(f"{c['name']} has no attack left this exchange: no harm (I8 / §12 ATTACK BUDGET) — treat as a setback")
        c["attacks_left"] -= 1
    tgt = Hurtable(ctx, a["target_id"])
    try:
        txt, _ = hit(ctx, tgt, a["kind"], a["size"], tgt.soak, a.get("hits", 1))
    except ValueError as e:
        raise ToolError(str(e))
    return txt


@tool("heal", "Restore HP or MP (§10.5). Rest uses the `rest` tool; this is for items, powers and treatment.",
      O({"target_id": S(), "pool": E("hp", "mp"), "mode": E("dice", "amount", "quarter", "full"),
         "dice": S("e.g. 2d6 (minor) 4d6 (standard)"), "amount": I("", 0), "reason": S("", minLength=4)},
        ["target_id", "pool", "mode", "reason"]))
def t_heal(ctx: TurnCtx, a):
    t = Hurtable(ctx, a["target_id"])
    cur, mx = (t.hp, t.max_hp) if a["pool"] == "hp" else (t.mp, t.max_mp)
    if cur is None: raise ToolError(f"{t.name} has no {a['pool'].upper()}")
    kw = dict(current=cur, max=mx, dice=None, amount=None, quarter=False, full=False)
    if a["mode"] == "dice": kw["dice"] = a.get("dice") or "2d6"
    elif a["mode"] == "amount": kw["amount"] = a.get("amount", 0)
    else: kw[a["mode"]] = True
    try:
        r = M().do_heal(helper.ns(**kw))
    except M().InputError as e:
        raise ToolError(str(e))
    (t.set_hp if a["pool"] == "hp" else t.set_mp)(r["current"])
    ctx.status.append(f"{t.name}: {a['pool'].upper()} {cur} → {r['current']}/{mx}")
    return f"{t.name} {a['pool'].upper()} {cur} → {r['current']} (max {mx})"


@tool("cast", "Pay an MP-drawing power's cost (§10.5): 3 × tier bonus, paid whether it works or not; no power above the caster's tier.",
      O({"tier": E("T1", "T2", "T3", "T4"), "power": S("", minLength=3)}, ["tier", "power"]))
def t_cast(ctx: TurnCtx, a):
    p = Hurtable(ctx, "player")
    if p.mp is None: raise ToolError("the player has no MP-drawing skill")
    if p.tier is None or rules.TIER_ORDER.index(a["tier"]) > rules.TIER_ORDER.index(p.tier):
        raise ToolError(f"no power above the caster's tier ({p.tier})")
    r = M().do_cast(helper.ns(mp=p.mp, tier=a["tier"]))
    if not r["cast"]:
        return f"NOT ENOUGH MP: needs {r['cost']}, has {p.mp}. The power cannot be cast."
    p.set_mp(r["mp"])
    ctx.status.append(f"MP {p.mp + r['cost']} → {r['mp']}/{p.max_mp} ({a['power']})")
    return f"cast paid: {r['cost']} MP; MP now {r['mp']}/{p.max_mp}. Whether the power works is a separate check if uncertain."


# =========================================================================================
def _due_items(ctx: TurnCtx) -> list[tuple[tuple[int, int], str, str]]:
    """Registered dues (plans and clocks) that have passed: (time, settle-key, description)."""
    camp = ctx.camp
    cal = timeutil.calendar_of(camp.bg)
    tree, out = ctx.tree(), []
    now = (int(camp.time["day_index"]), int(camp.time["clock_minutes"]))
    for owner in ("npcs", "factions"):
        for k, v in (tree.get(owner) or {}).items():
            st = (v or {}).get("state") if isinstance(v, dict) else None
            if not isinstance(st, dict) or not st.get("due"): continue
            pts = timeutil.due_points(str(st["due"]), camp.time, cal)
            if pts and min(pts) <= now:
                out.append((min(pts), f"due:{owner}.{k}",
                            f"{v.get('name', k)} ({owner}.{k}): plan '{st.get('plan', '?')}' was due {st['due']}"))
    for k, v in (tree.get("active_world_pressures") or {}).items():
        ck = (v or {}).get("clock") if isinstance(v, dict) else None
        if isinstance(ck, dict) and ck.get("due"):
            pts = timeutil.due_points(str(ck["due"]), camp.time, cal)
            if pts and min(pts) <= now and int(ck.get("filled", 0)) < int(ck.get("segments", 1)):
                out.append((min(pts), f"clock:{k}", f"pressure {k}: clock '{ck.get('name')}' due {ck['due']} "
                            f"(filled {ck.get('filled')}/{ck.get('segments')}, pace: {ck.get('pace')})"))
    return sorted(out)


def _advance(ctx: TurnCtx, minutes: int, date=None, season=None) -> list[str]:
    camp = ctx.camp
    try:
        new, rolled = timeutil.advance(camp.time, minutes, date, season)
    except ValueError as e:
        raise ToolError(str(e))
    camp.readable["world_state"]["time"] = new
    notes = []
    for _, key, desc in _due_items(ctx):
        if key not in ctx.must_settle:
            ctx.must_settle[key] = desc
            notes.append(desc)
    return notes


@tool("advance_time", "Move world time forward (§13.2) by a believable duration. The host does the clock and calendar maths "
      "and lists every plan/clock that is now DUE; you must resolve each before closing the round. "
      "Pass `date` (the setting's own calendar) if a day rolls over and the calendar is not ISO.",
      O({"minutes": I("", 0, 100000), "activity": S("what takes the time", minLength=3),
         "date": S("new date string if the day rolls over (setting's calendar format)"), "season": S()},
        ["minutes", "activity"]))
def t_advance_time(ctx: TurnCtx, a):
    notes = _advance(ctx, a["minutes"], a.get("date"), a.get("season"))
    t = ctx.camp.time
    out = f"time is now {timeutil.date_label(t)} {timeutil.hhmm(t['clock_minutes'])} ({t['daypart']})."
    if notes:
        out += "\nDUE NOW (earliest first; resolve each — REPLAN with a new `state.due`, or clock_check):\n- " + "\n- ".join(notes)
    out += ("\nIf the player moved or meaningful time passed where change is possible, consider §13.3 "
            "(roll kind=ambient only if the setting supports background uncertainty here).")
    return out


@tool("rest", "Rest or sleep (§10.5 RECOVERY): HP/MP recovery and time passing are computed by the host. Lasting injuries never heal by rest.",
      O({"hours": I("", 1, 24), "quality": E("short", "full_night", "tended"),
         "out_of_danger": B("needed for fast MP recovery"), "date": S("new date if a day rolls over (non-ISO calendars)")},
        ["hours", "quality"]))
def t_rest(ctx: TurnCtx, a):
    camp, m = ctx.camp, M()
    p = Hurtable(ctx, "player")
    if p.hp <= 0:
        raise ToolError("the player is down: only treatment helps (heal), or the down_check roll after 1 hour untreated")
    notes = _advance(ctx, a["hours"] * 60, a.get("date"))
    before_hp, before_mp = p.hp, p.mp
    if a["quality"] == "short":
        for _ in range(a["hours"]):
            p.set_hp(m.do_heal(helper.ns(current=p.hp, max=p.max_hp, dice=None, amount=None, quarter=True, full=False))["current"])
    else:
        p.set_hp(p.max_hp)
    rec = ((camp.bg.get("setting_anchors") or {}).get("mp_powers") or {}).get("recovery", "rest_only")
    if p.mp is not None:
        if rec == "fast" and a.get("out_of_danger"): p.set_mp(p.max_mp)
        elif rec == "slow":
            for _ in range(a["hours"]):
                p.set_mp(m.do_heal(helper.ns(current=p.mp, max=p.max_mp, dice=None, amount=None, quarter=True, full=False))["current"])
        elif a["quality"] != "short": p.set_mp(p.max_mp)
    camp.player["condition"]["last_rest"] = f"{timeutil.date_label(camp.time)} {timeutil.hhmm(camp.time['clock_minutes'])}, {a['quality']}"
    ctx.status.append(f"rest: HP {before_hp} → {p.hp}/{p.max_hp}" + (f", MP {before_mp} → {p.mp}/{p.max_mp}" if p.mp is not None else ""))
    out = f"rested {a['hours']}h ({a['quality']}). HP {before_hp} → {p.hp}/{p.max_hp}" + (f"; MP {p.mp}/{p.max_mp}" if p.mp is not None else "") + "."
    if a["quality"] != "short":
        out += ("\nSubstantial sleep is a GROWTH BOUNDARY (§11.1): call growth_boundary now. Reduce fatigue with player_update if justified. "
                "Lasting injuries: only real treatment removes them.")
    if notes:
        out += "\nDUE NOW:\n- " + "\n- ".join(notes)
    return out


# =========================================================================================
@tool("award_xp", "Award XP (Part 2 §A, module numeric_level_xp). The host derives each participant's award from the challenge R, "
      "their own level P and the scope, sums several enemies once, refuses a scope that already paid, and applies level-ups.",
      O({"kind": E("combat", "event", "quest"), "scope_id": S("stable id of the resolved encounter/event/quest/segment", minLength=3),
         "scope": E("routine", "minor", "meaningful", "major", "exceptional"),
         "challenges": A(I("actual challenge R of one overcome enemy/task", 1, 60), minItems=1, maxItems=20),
         "participants": A(S("`player` or a tracked companion npc id"), minItems=1)},
        ["kind", "scope_id", "scope", "challenges", "participants"]))
def t_award_xp(ctx: TurnCtx, a):
    camp, m = ctx.camp, M()
    if not camp.numeric:
        raise ToolError("numeric_level_xp is not enabled: there is no XP in this campaign")
    marker = f"world_state.material_history.xp_{a['scope_id']}"
    if ctx.get(marker):
        raise ToolError(f"scope {a['scope_id']!r} has already paid XP (I8: never paid twice)")
    lines, total_paid = [], {}
    for pid in a["participants"]:
        if pid == "player":
            st = camp.player["progression"]["state"]
        else:
            npc = ctx.get(f"npcs.{pid}")
            prog = ((npc or {}).get("capability") or {}).get("progression") if isinstance(npc, dict) else None
            if not isinstance(prog, dict) or "state" not in prog:
                raise ToolError(f"npcs.{pid} is not a tracked participant (needs capability.progression.state {{level, xp}})")
            st = dict(prog["state"])
        level, xp = int(st["level"]), int(st.get("xp", 0))
        try:
            award = sum(m.do_xp(helper.ns(level=level, xp=xp, r=r, p=level, scope=a["scope"], amount=None))["award"]
                        for r in a["challenges"])
            res = m.do_xp(helper.ns(level=level, xp=xp, r=None, p=None, scope=None, amount=award))
        except m.InputError as e:
            raise ToolError(str(e))
        new = res["new"]
        if pid == "player":
            st.update(new)
        else:
            ctx.add_entry("~", f"npcs.{pid}.capability.progression", {"system": "numeric_level_xp", "state": new}, hidden=False)
        total_paid[pid] = award
        who = "XP" if pid == "player" else f"{pid} XP"
        ups = f"; LEVEL UP → {res['level_ups'][-1]}" if res["level_ups"] else ""
        line = f"{who} +{award} → level {new['level']} ({new['xp']}/{res.get('next_requirement') or '—'}){ups}"
        lines.append(line)
        if pid == "player" and award:
            ctx.status.append(line)
    ctx.add_entry("+", marker, f"paid {json.dumps(total_paid)} for {a['kind']} {a['scope']} (R{camp.rnd + 1})", hidden=False)
    return "\n".join(lines) + "\n(payout marker written; this scope cannot pay again)"


@tool("growth_boundary", "A growth boundary (§11.1): substantial rest, dedicated training, or a settled arc. The host resolves "
      "accumulated skill evidence into tier raises (and class raises where a valid class source was involved) and opens a new period.",
      O({"class_sources": A(S(), "skill ids whose class raise has a valid class source materially involved (§11.2)"),
         "reason": S("", minLength=5)}, ["reason"]))
def t_growth_boundary(ctx: TurnCtx, a):
    camp, m = ctx.camp, M()
    out = []
    for sid, sk in camp.player.get("skills", {}).items():
        r = m.do_boundary(helper.ns(cls=sk["class"], tier=sk["tier"], evidence=int(sk.get("growth_evidence", 0)),
                                    ceiling_evidence=int(sk.get("ceiling_evidence", 0)),
                                    class_source=sid in (a.get("class_sources") or [])))
        new = r["new"]
        changed = r["raised"] or r.get("class_raised")
        sk.update({"tier": new["tier"], "class": new["class"], "growth_evidence": new["growth_evidence"],
                   "ceiling_evidence": new["ceiling_evidence"]})
        if r.get("class_raised"):
            sk["class_source"] = "class source involved at boundary"
        if changed:
            note = f"{sid}: tier {r['raised'][-1] if r['raised'] else sk['tier']}" + (f", class {r['class_raised']}" if r.get("class_raised") else "")
            ctx.learned.append(f"quiet noticed change — {note}")
            out.append(note)
    camp.player["growth_period"] = {"opened": camp.time["day_index"], "credited": []}
    inj = camp.player["condition"].get("injuries") or []
    msg = "boundary resolved. " + ("Raised: " + "; ".join(out) if out else "No tier changes.")
    if inj:
        msg += f"\nLasting injuries to check now (removal needs real treatment for its time, as its own player_update injury_remove): {json.dumps(inj, ensure_ascii=False)}"
    return msg + "\nNarrate any raise as a quiet noticed change, never mid-action."


# =========================================================================================
_ENTRY = O({"op": E("+", "~", "-"), "id": S("<owner>.<record>.<field>, e.g. npcs.hadvar.state.position", minLength=3),
            "content": S("one line: who, why, what evidence exists where — not the reveal or the scene", minLength=1),
            "hidden": B("true unless the player has perceived/learned this fact"),
            "secret_terms": A(S(), "distinct words that would give away a hidden fact if narrated (checked against the prose)", maxItems=6)},
           ["op", "id", "content"])
_ID = re.compile(r"^[A-Za-z_][\w\-]*(\.[\w\-]+)*$")
_READABLE = ("player", "world_state.time", "world_state.location", "world_state.environment",
             "enabled_modules", "narrative_theme")
_REQUIRED_IDENTITY = {"npcs": ("name", "job", "belongs", "gender", "character"), "factions": ("name", "role")}
_FIELD_RECORD_OWNERS = {"npcs", "factions", "quests", "locations", "active_world_pressures",
                        "locked_case_truths", "rights_obligations", "development_threads", "trackers", "open_suspicions"}


@tool("commit", "Write capsule records as GM-Δ entries (§8.1). A fact exists only once written. `+` new path / new record (one line holds its "
      "whole content as JSON), `~` new value of a NAMED FIELD, `-` no longer holds (content = why). Cause first (I2): commit the hidden cause "
      "before anything that depends on it. Never file player/time/location here (use player_update / advance_time).",
      O({"entries": A(_ENTRY, minItems=1, maxItems=20)}, ["entries"]))
def t_commit(ctx: TurnCtx, a):
    m, notes = M(), []
    for e in a["entries"]:
        op, rid, content = e["op"], e["id"], re.sub(r"\s+", " ", str(e["content"])).strip()
        if not _ID.match(rid): raise ToolError(f"bad id {rid!r}: dotted [A-Za-z0-9_-] segments, starting with a letter")
        owner = rid.split(".")[0]
        if any(rid == p or rid.startswith(p + ".") for p in _READABLE):
            raise ToolError(f"{rid}: the readable save holds that (player_update / advance_time / location tools)")
        if owner not in CAPSULE_OWNERS:
            raise ToolError(f"{rid}: {owner!r} is not an engine owner (§6). Owners: {sorted(CAPSULE_OWNERS)}")
        if not content or content.startswith("enc:"):
            raise ToolError(f"{rid}: content must be plain text (the host encodes if the player asked)")
        depth = rid.count(".")
        if op == "~" and owner in _FIELD_RECORD_OWNERS and depth == 1:
            raise ToolError(f"{rid}: name the field you change, e.g. {rid}.state.position (a whole record is never overwritten)")
        if op == "+" and owner in _REQUIRED_IDENTITY and depth == 1:
            try:
                obj = json.loads(content)
            except Exception:
                raise ToolError(f"{rid}: a new {owner[:-1]} record must be one JSON object line")
            miss = [k for k in _REQUIRED_IDENTITY[owner] if k not in obj]
            if miss: raise ToolError(f"{rid}: required identity fields missing: {miss} (use \"unknown\" where play has not established one)")
            if ctx.get(rid) is None and owner == "npcs":
                # TEMPER (§13.1): once per new non-BACKGROUND actor
                opposing = bool(e.get("hidden") is False and obj.get("opposing"))
                r = m.roll_spec("2d10")
                need = 15 if opposing else 17
                if r["sum"] >= need:
                    ctx.must_settle[f"temper:{rid}"] = (f"TEMPER roll {r['sum']} ≥ {need}: {obj.get('name')} is a DIFFICULT character fitting the role "
                                                        f"(rude, greedy, petty, bully…). Commit `+ {rid}.temper :: <how it shows>` (permanent; never aimed at the player's secrets)")
                    notes.append(f"TEMPER for {rid}: difficult — add {rid}.temper")
                else:
                    ctx.add_entry("+", f"{rid}.temper", "ordinary (rolled at creation)", hidden=True)
        if op == "-" and not content:
            raise ToolError(f"{rid}: `-` needs the reason as content")
        ctx.add_entry(op, rid, content, bool(e.get("hidden", True)), e.get("secret_terms"))
        ctx.secret_terms.update(t.lower() for t in e.get("secret_terms") or [] if len(t) > 2)
        if rid.endswith(".temper"):
            ctx.settle("temper:" + rid[:-len(".temper")])
        mi = re.match(r"npcs\.([\w\-]+)\.state\.injur", rid)
        if mi:
            ctx.settle(f"injury:{mi.group(1)}")
        if rid.endswith(".state.due") or rid.endswith(".state"):
            ctx.settle(f"due:{rid.rsplit('.state', 1)[0]}")
        if rid.startswith("active_world_pressures.") and ".clock" in rid:
            ctx.settle("clock:" + rid.split(".")[1])
    return f"committed {len(a['entries'])} entr{'y' if len(a['entries']) == 1 else 'ies'}." + ("\n" + "\n".join(notes) if notes else "")


@tool("clock_check", "Advance a pressure clock at its due check (§13.5). Fill ONE segment only if the process actually operated; "
      "a plainly accelerating event may fill one extra. The host does the arithmetic and writes the entries.",
      O({"pressure_id": S(), "process_operated": B("false if actors stopped/absent/out of resources/no opportunity"),
         "accelerated": B("an event plainly accelerated it"), "next_due": S("next check time, in the setting's date format"),
         "reason": S("", minLength=5)}, ["pressure_id", "process_operated", "next_due", "reason"]))
def t_clock_check(ctx: TurnCtx, a):
    pid = a["pressure_id"]
    p = ctx.get(f"active_world_pressures.{pid}")
    ck = (p or {}).get("clock") if isinstance(p, dict) else None
    if not isinstance(ck, dict): raise ToolError(f"pressure {pid!r} has no clock")
    seg, filled = int(ck["segments"]), int(ck.get("filled", 0))
    add = (1 if a["process_operated"] else 0) + (1 if a["process_operated"] and a.get("accelerated") else 0)
    new = min(seg, filled + add)
    pts = timeutil.due_points(a["next_due"], ctx.camp.time, timeutil.calendar_of(ctx.camp.bg))
    if not pts: raise ToolError("next_due must be a date the host can read (same format as the current date, e.g. 2026-03-06 06:00)")
    if min(pts) <= (ctx.camp.time["day_index"], ctx.camp.time["clock_minutes"]):
        raise ToolError("next_due must be in the future")
    base = f"active_world_pressures.{pid}.clock"
    ctx.add_entry("~", f"{base}.filled", str(new), hidden=True)
    ctx.add_entry("~", f"{base}.due", a["next_due"], hidden=True)
    ctx.settle(f"clock:{pid}")
    out = f"clock '{ck.get('name')}' {filled} → {new}/{seg}; next check {a['next_due']}."
    if new >= seg:
        out += f"\nFULL: on_fill happens now, present or not: {ck.get('on_fill')}. Commit its consequences; the player learns only via a real channel (I5)."
    return out


# =========================================================================================
@tool("roll", "Engine dice that are not checks. shape: quest shape 1d10 (1-7 SHORT, 8-9 LONG, 10 CHAIN) · chain_first: 1d4 (1-3 SHORT, 4 LONG) · "
      "ambient: §13.3 1d10 (9-10 incident) then weight · temper: 2d10 ≥17 (≥15 opposing) · down_check: 2d10 ≥11 wakes at 1 HP else dies · "
      "pick: choose among n equally fitting causes.",
      O({"kind": E("shape", "chain_first", "ambient", "down_check", "pick"), "n": I("for pick: number of fits", 2, 20),
         "target_id": S("for down_check: who")}, ["kind"]))
def t_roll(ctx: TurnCtx, a):
    m, k = M(), a["kind"]
    if k == "shape":
        v = m.roll_spec("1d10")["sum"]; return f"shape roll {v} → " + ("SHORT" if v <= 7 else "LONG" if v <= 9 else "CHAIN") + " (generation dice are transient, unsaved)"
    if k == "chain_first":
        v = m.roll_spec("1d4")["sum"]; return f"first-child roll {v} → " + ("SHORT" if v <= 3 else "LONG")
    if k == "pick":
        if "n" not in a: raise ToolError("pick needs n")
        return f"pick → option {m.roll_spec('1d' + str(a['n']))['sum']} of {a['n']}"
    if k == "ambient":
        v = m.roll_spec("1d10")["sum"]
        if v <= 8: return f"ambient 1d10 = {v}: nothing happens this transition"
        w = m.roll_spec("1d10")["sum"]
        wt = "MINOR" if w <= 5 else "MODERATE" if w <= 8 else "MAJOR" if w == 9 else "EXCEPTIONAL"
        return (f"ambient 1d10 = {v}: AMBIENT INCIDENT, weight 1d10 = {w} → {wt}. Choose the cause from the pool FIRST "
                "(roll kind=pick among fits) without looking at what the player carries or hides, then size it; commit the cause before evidence (I2).")
    if k == "down_check":
        t = Hurtable(ctx, a.get("target_id") or "player")
        if t.hp > 0: raise ToolError(f"{t.name} is not down")
        v = m.roll_spec("2d10")["sum"]
        if v >= 11:
            t.set_hp(1)
            return f"down_check 2d10 = {v} ≥ 11: {t.name} wakes at 1 HP"
        if t.kind == "player":
            ctx.camp.session["ended"] = True; ctx.camp.player["status"] = "dead"
        return f"down_check 2d10 = {v} < 11: {t.name} DIES"
    raise ToolError("unknown roll kind")


# =========================================================================================
_PU_KINDS = ("money", "resource", "equipment", "injury_add", "injury_remove", "fatigue", "status",
             "fighting_style", "routine", "knowledge", "skill_add", "location", "environment", "theme")


@tool("player_update", "Change the player block (the readable save). HP/MP/XP/skill evidence have their own tools and cannot be set here. "
      "kinds & data: money {delta: int | {coin: int}} · resource {resource_id, op: spend|gain|draw|resupply_die|add, amount?, die?, name?, tracking?} · "
      "equipment {op: add|remove|condition, item: {item_id,name,type,capability_domain,condition,special_properties,abilities}} · "
      "injury_add {injury, home, effect} · injury_remove {injury, treatment} · fatigue {value} · status {value} · "
      "fighting_style {habit} (ONLY when the player stated it) · routine {id, action, recurrence, condition, status} · "
      "knowledge {key, value, channel} · skill_add {skill_id, class, tier:T1, reason} · location {id} · environment {key, value} · theme {tone, style}",
      O({"kind": E(*_PU_KINDS), "data": O(), "reason": S("", minLength=5)}, ["kind", "data", "reason"]))
def t_player_update(ctx: TurnCtx, a):
    camp, m = ctx.camp, M()
    p, d, k = camp.player, a["data"], a["kind"]
    if k == "money":
        delta = d.get("delta")
        if isinstance(p.get("money"), dict) and "cash_and_accessible_funds" in p["money"] and isinstance(delta, int):
            new = int(p["money"]["cash_and_accessible_funds"]) + delta
            if new < 0: raise ToolError(f"not enough money: has {new - delta}")
            p["money"]["cash_and_accessible_funds"] = new
        elif isinstance(p.get("money"), dict) and isinstance(delta, dict):
            new = dict(p["money"])
            for coin, v in delta.items():
                if coin not in new and v < 0: raise ToolError(f"player has no {coin}")
                new[coin] = new.get(coin, 0) + int(v)
                if new[coin] < 0: raise ToolError(f"not enough {coin}: has {new[coin] - int(v)}, needs {-int(v)}")
            p["money"] = new
        elif isinstance(delta, int) and not isinstance(p.get("money"), dict):
            new = int(p.get("money") or 0) + delta
            if new < 0: raise ToolError(f"not enough money: has {new - delta}")
            p["money"] = new
        else:
            raise ToolError("money delta must match the money shape: " + json.dumps(p.get("money")))
        ctx.status.append(f"money → {json.dumps(p['money'], ensure_ascii=False)}")
        return f"money now {p['money']}"
    if k == "resource":
        rid, op = d.get("resource_id"), d.get("op")
        res = p.setdefault("resources", {})
        if op == "add":
            if rid in res: raise ToolError(f"resource {rid!r} exists")
            r = {"name": d.get("name", rid), "tracking": d.get("tracking", "exact")}
            if r["tracking"] == "exact": r["count"] = int(d.get("amount", 0))
            else: r["usage_die"] = d.get("die", "d6")
            res[rid] = r; return f"resource {rid} added: {r}"
        r = res.get(rid)
        if r is None: raise ToolError(f"unknown resource {rid!r}; known: {list(res)}")
        if r["tracking"] == "exact":
            if op not in ("spend", "gain"): raise ToolError("exact resources use op spend|gain")
            n = int(d.get("amount", 0))
            new = r["count"] + (n if op == "gain" else -n)
            if new < 0: raise ToolError(f"not enough {r['name']}: has {r['count']}")
            r["count"] = new; ctx.status.append(f"{r['name']}: {new}"); return f"{r['name']} now {new}"
        order = ["d12", "d10", "d8", "d6", "d4", "empty"]
        if op == "draw":
            cur = r["usage_die"]
            if cur == "empty": raise ToolError(f"{r['name']} is exhausted")
            roll = m.roll_spec("1" + cur)["sum"]
            if roll <= 2:
                r["usage_die"] = order[order.index(cur) + 1]
                ctx.status.append(f"{r['name']}: usage die {cur} → {r['usage_die']}")
                return f"usage die {cur}: rolled {roll} → steps down to {r['usage_die']}"
            return f"usage die {cur}: rolled {roll} → holds"
        if op == "resupply_die":
            nd = d.get("die")
            if nd not in order[:-1] or order.index(nd) >= order.index(r["usage_die"]): raise ToolError("resupply must raise the die (real resupply only; it never refills itself)")
            r["usage_die"] = nd; return f"{r['name']} resupplied to {nd}"
        raise ToolError("usage_die resources use op draw|resupply_die")
    if k == "equipment":
        eq, op, it = p.setdefault("equipment", []), d.get("op"), d.get("item") or {}
        if op == "add":
            miss = [f for f in ("item_id", "name", "type", "capability_domain", "condition") if f not in it]
            if miss: raise ToolError(f"equipment item missing {miss}")
            if it["condition"] not in ("serviceable", "worn", "damaged", "critical"): raise ToolError("condition: serviceable|worn|damaged|critical")
            if any(x["item_id"] == it["item_id"] for x in eq): raise ToolError(f"item {it['item_id']} exists")
            it.setdefault("special_properties", []); it.setdefault("abilities", [])
            eq.append(it); return f"added {it['name']}"
        i = next((x for x in eq if x["item_id"] == it.get("item_id")), None)
        if i is None: raise ToolError(f"no item {it.get('item_id')!r}; have {[x['item_id'] for x in eq]}")
        if op == "remove": eq.remove(i); return f"removed {i['name']}"
        if op == "condition":
            if it.get("condition") not in ("serviceable", "worn", "damaged", "critical"): raise ToolError("condition: serviceable|worn|damaged|critical")
            i["condition"] = it["condition"]; return f"{i['name']} is now {it['condition']} (real repair needs time, skill, tools — never silent)"
        raise ToolError("equipment op: add|remove|condition")
    if k == "injury_add":
        if d.get("home") not in rules.INJURY_HOMES or not d.get("effect") or not d.get("injury"):
            raise ToolError(f"an injury needs injury, effect and exactly one home from {rules.INJURY_HOMES} (I8)")
        p["condition"].setdefault("injuries", []).append({"injury": d["injury"], "home": d["home"], "effect": d["effect"]})
        ctx.settle("injury:player"); return "lasting injury recorded"
    if k == "injury_remove":
        inj = p["condition"].get("injuries") or []
        i = next((x for x in inj if x["injury"] == d.get("injury")), None)
        if i is None: raise ToolError(f"no such injury; have {[x['injury'] for x in inj]}")
        if not d.get("treatment"): raise ToolError("removal needs real treatment for its time (healer, restoration power, strong healing item, tended rest)")
        inj.remove(i); return f"injury removed after: {d['treatment']}"
    if k in ("fatigue", "status"):
        if "value" not in d: raise ToolError("data.value required")
        (p["condition"] if k == "fatigue" else p).__setitem__(k, d["value"]); return f"{k} = {d['value']}"
    if k == "fighting_style":
        if not d.get("habit"): raise ToolError("data.habit required")
        p.setdefault("fighting_style", []).append(d["habit"]); ctx.status.append(f"Fighting style: {d['habit']}")
        return f"Fighting style: {d['habit']}"
    if k == "routine":
        rid = d.get("id")
        if not rid or not d.get("action"): raise ToolError("routine needs id and action (in-world recurring behaviour only)")
        p.setdefault("routines", {})[rid] = {x: d[x] for x in ("action", "recurrence", "condition", "status") if x in d}; return f"routine {rid} set"
    if k == "knowledge":
        if not d.get("key"): raise ToolError("data.key required")
        p.setdefault("knowledge", {}).setdefault("facts", {})[d["key"]] = d.get("value", "")
        if d.get("channel"):
            ch = p["knowledge"].setdefault("channels", [])
            if d["channel"] not in ch: ch.append(d["channel"])
        return f"player now knows {d['key']}"
    if k == "skill_add":
        sid = d.get("skill_id")
        if not sid or sid in p.setdefault("skills", {}): raise ToolError("skill_id required and must be new")
        if d.get("tier", "T1") != "T1": raise ToolError("a newly learned skill starts at T1")
        p["skills"][sid] = {"class": d.get("class", "NORMAL"), "tier": "T1", "growth_evidence": 0, "ceiling_evidence": 0, "abilities": []}
        return f"skill {sid} added at T1"
    if k == "location":
        lid = d.get("id")
        loc = ctx.get(f"locations.{lid}")
        if not isinstance(loc, dict): raise ToolError(f"unknown location {lid!r}: commit `+ locations.{lid}` first, with name, conditions and challenge_band (§13.4)")
        if not (loc.get("challenge_band") or {}).get("basis"):
            raise ToolError(f"locations.{lid} has no committed challenge_band {{min,max,basis}}; derive it from settlement size, institutions, threats (never the player's level) and commit it first (§13.4)")
        camp.readable["world_state"]["location"] = lid; return f"location = {loc.get('name', lid)}"
    if k == "environment":
        camp.readable["world_state"]["environment"][d.get("key", "note")] = d.get("value", ""); return "environment updated"
    if k == "theme":
        camp.readable["narrative_theme"]["current"] = {x: d[x] for x in ("tone", "style") if x in d}; return "theme updated (explicit request or in-world shift only)"
    raise ToolError("unknown kind")


@tool("spend_item_points", "Module D (flexible_item_entitlement): the player spends points to make one useful unestablished detail true about "
      "their own possessions. You supply the single plausible in-world reason; the host checks the reserve and charges once.",
      O({"cost": I("0,1,2,4,8,16 per §D", 0, 64), "what": S("the item/property now true", minLength=5),
         "reason": S("the committed in-world source (carried/packed, earlier gift, found within reach, …) consistent with all established facts", minLength=12)},
        ["cost", "what", "reason"]))
def t_spend(ctx: TurnCtx, a):
    camp = ctx.camp
    if not camp.modules.get("flexible_item_entitlement"): raise ToolError("flexible_item_entitlement is not enabled")
    have = int(camp.player.get("item_points", 0))
    if a["cost"] > have: raise ToolError(f"reserve {have} < cost {a['cost']}: the spend fails, costs 0, commits nothing")
    camp.player["item_points"] = have - a["cost"]
    ctx.add_entry("+", f"world_state.material_history.item_spend_r{camp.rnd + 1}", f"{a['what']} — source: {a['reason']}", hidden=False)
    return f"spent {a['cost']}: item points {have} → {have - a['cost']}. Add the item with player_update equipment; narrate the reason as what happened."


# =========================================================================================
_LEARN = O({"section": E(*INDEX_SECTIONS), "id": S(), "line": S("one line: what the player knows, a few words", minLength=3)},
           ["section", "id", "line"])
_CLOSE = O({
    "opened_round": B("true if this was a new material player action resolved as a ROUND; false for FAST actions, retrieval, clarifications, an odds-stop or a decision still open"),
    "visible": A(S(), "everything the player observes this turn, in order, concrete and in English (no hidden causes, no hidden state)", minItems=1, maxItems=30),
    "dialogue": A(O({"who": S(), "gist": S("what they say/mean, in a few words"), "tone": S()}, ["who", "gist"])),
    "player_learned": A(_LEARN, "index lines for records the player now knows of (the id must exist in the ledger)"),
    "decision": O({"question": S("the real DECISION (§2): conflict, cost, danger, important offer…"), "options": A(S(), minItems=2, maxItems=5)},
                  desc="only when a real DECISION exists; never where orders/fighting_style already answer it"),
    "plan": S("the plan/orders now in force for the current action or fight; empty string clears it"),
    "new_terms": A(O({"id": S(), "english": S(), "form": S()}, ["id", "english", "form"]), "new names/terms in the game language (AI_RULES Language)"),
}, ["opened_round", "visible"])


@tool("close_round", "FINISH this turn. The host then builds the header, GM-Δ block and narration. Refused while the host still lists items to settle "
      "(due plans/clocks, lasting injuries, temper, a downed player).", _CLOSE)
def t_close(ctx: TurnCtx, a):
    camp = ctx.camp
    if ctx.check_refused and not ctx.rolled and not ctx.close_warned:
        ctx.close_warned = True
        raise ToolError("your roll (check/ask) was REFUSED and nothing was rolled. If this action is uncertain, call it again with the "
                        "corrected arguments (a dropped roll is a hidden success: I10). If it truly needs no roll, call close_round again.")
    if ctx.must_settle:
        raise ToolError("cannot close yet — settle these first:\n- " + "\n- ".join(ctx.must_settle.values()))
    if ctx.stopped_for_odds and a["opened_round"]:
        raise ToolError("an odds-stop leaves the action unresolved: opened_round must be false")
    if a["opened_round"] is False and ctx.rolled:
        raise ToolError("a turn with a resolved roll is a ROUND: set opened_round=true")
    for L in a.get("player_learned") or []:
        if ctx.get(f"{L['section']}.{L['id']}") is None:
            raise ToolError(f"index line for {L['section']}.{L['id']}: that record does not exist; commit it first (I3)")
    lang = camp.language
    for t in a.get("new_terms") or []:
        ctx.add_entry("+", f"world_state.glossary.{lang}.{t['id']}", f"{t['english']} = {t['form']}", hidden=False)
    ctx.closed = a
    return "closed"
