"""Semantic audit of a campaign state: rules the helper's `validate` does not check.

`validate` proves a save is well-formed and nothing was dropped. This checks that the numbers obey the engine
(vitals, XP, skill tiers, evidence, injuries, usage dice, clocks, quest levels, index references, time).
"""
from __future__ import annotations
import re
from dataclasses import dataclass

from . import helper, rules, timeutil
from .campaign import Campaign, CAPSULE_OWNERS

XP_REQ = None
GROWTH = {"T1": 10, "T2": 20, "T3": 40}
CLASS_T = {"NORMAL": 20, "ELITE": 40}
ABIL = {"T1": (0, 0), "T2": (0, 1), "T3": (2, 3), "T4": (1, 1)}


@dataclass
class Finding:
    level: str      # error | warn | info
    area: str
    msg: str

    def __str__(self): return f"[{self.level.upper():5}] {self.area}: {self.msg}"


def audit(camp: Campaign) -> list[Finding]:
    m = helper.mod()
    out: list[Finding] = []
    def add(level, area, msg): out.append(Finding(level, area, msg))
    rd, p, mods = camp.readable, camp.player, camp.modules
    tree = camp.tree()
    numeric = bool(mods.get("numeric_level_xp"))
    # ---- round / time ------------------------------------------------------------------------
    r = rd.get("round", {})
    if r.get("last_completed_round") != r.get("saved_completed_round"):
        add("warn", "round", f"last_completed {r.get('last_completed_round')} != saved {r.get('saved_completed_round')}")
    t = camp.time
    if t.get("precision") not in ("exact", "daypart", "degraded"): add("error", "time", f"bad precision {t.get('precision')!r}")
    if not 0 <= int(t.get("clock_minutes", -1)) <= 1439: add("error", "time", "clock_minutes outside 0..1439")
    cal = timeutil.calendar_of(camp.bg)
    start = ((camp.bg.get("world_state") or {}).get("time") or {})
    iso0 = timeutil.ISO.match(str(start.get("date") or "")); iso1 = timeutil.ISO.match(str(t.get("date") or ""))
    if iso0 and iso1:
        import datetime as dt
        d0 = dt.date(*map(int, iso0.groups())); d1 = dt.date(*map(int, iso1.groups()))
        want = int(start.get("day_index", 0)) + (d1 - d0).days
        if want != int(t["day_index"]): add("error", "time", f"day_index {t['day_index']} disagrees with date {t['date']} (expected {want})")
    # ---- player vitals / progression ------------------------------------------------------------
    v = rules.vitality_value(p, numeric)
    draws = ((camp.bg.get("setting_anchors") or {}).get("mp_powers") or {}).get("draws_mp") or []
    tier = rules.mp_tier(p, draws)
    mx = rules.max_vitals(v, "normal", tier)
    c = p.get("condition", {})
    if int(c.get("hp", 0)) > mx["max_hp"]: add("error", "vitals", f"hp {c['hp']} above derived max {mx['max_hp']}")
    if int(c.get("hp", 0)) < 0: add("error", "vitals", "negative hp")
    if "mp" in c and tier is None: add("warn", "vitals", "mp is saved but no MP-drawing skill is recognised (setting_anchors.mp_powers.draws_mp)")
    if tier and int(c.get("mp", 0)) > mx["max_mp"]: add("error", "vitals", f"mp {c['mp']} above derived max {mx['max_mp']}")
    if numeric:
        st = (p.get("progression") or {}).get("state") or {}
        lvl, xp = st.get("level"), st.get("xp")
        if not isinstance(lvl, int) or not 1 <= lvl <= 35: add("error", "progression", f"level {lvl!r} outside 1..35")
        else:
            req = m.XP_REQ.get(lvl)
            if lvl == 35 and xp != 0: add("error", "progression", "level 35 must carry xp 0")
            if req is not None and int(xp) >= req: add("error", "progression", f"xp {xp} >= {req}: a level-up was not carried")
        if "vitality" in p: add("warn", "progression", "vitality saved while numeric_level_xp is on")
    else:
        if "progression" in p: add("error", "progression", "progression present but numeric_level_xp is off")
        if p.get("vitality") not in rules.VITALITY: add("error", "vitality", f"vitality {p.get('vitality')!r} not in {list(rules.VITALITY)}")
    # ---- skills ----------------------------------------------------------------------------------
    for sid, sk in (p.get("skills") or {}).items():
        cls, tr = sk.get("class"), sk.get("tier")
        if cls not in rules.CEILING or tr not in rules.TIER_ORDER:
            add("error", f"skill {sid}", f"bad class/tier {cls}/{tr}"); continue
        ceil = rules.CEILING[cls]
        if rules.TIER_ORDER.index(tr) > rules.TIER_ORDER.index(ceil): add("error", f"skill {sid}", f"tier {tr} above class {cls} ceiling {ceil}")
        ge, ce = int(sk.get("growth_evidence", 0)), int(sk.get("ceiling_evidence", 0))
        if ge < 0 or ce < 0: add("error", f"skill {sid}", "negative evidence")
        if tr != ceil and ge >= GROWTH[tr]: add("warn", f"skill {sid}", f"growth_evidence {ge} >= {GROWTH[tr]}: a growth boundary is unresolved")
        if tr == ceil and ge: add("warn", f"skill {sid}", "growth_evidence at ceiling should be ceiling_evidence")
        if cls in CLASS_T and ce >= CLASS_T[cls]: add("info", f"skill {sid}", f"ceiling_evidence {ce} >= {CLASS_T[cls]}: needs a class source to raise")
        lo, hi = ABIL[tr]; n = len(sk.get("abilities") or [])
        if not lo <= n <= hi: add("warn", f"skill {sid}", f"{n} abilities at {tr} (engine §11.2 allows {lo}-{hi})")
    gp = p.get("growth_period") or {}
    for sid in gp.get("credited", []):
        if sid not in (p.get("skills") or {}): add("error", "growth_period", f"credited skill {sid!r} does not exist")
    # ---- equipment / resources / injuries / item points ---------------------------------------
    for it in p.get("equipment") or []:
        if it.get("condition") not in ("serviceable", "worn", "damaged", "critical"): add("error", f"item {it.get('item_id')}", f"condition {it.get('condition')!r}")
        if mods.get("equipment_power_tiers") and it.get("tier") not in rules.TIER_ORDER: add("warn", f"item {it.get('item_id')}", "equipment tiers enabled but tier missing/invalid")
        if not mods.get("equipment_power_tiers") and it.get("tier"): add("warn", f"item {it.get('item_id')}", "tier saved but equipment_power_tiers is off")
    for rid, rs in (p.get("resources") or {}).items():
        tr = rs.get("tracking")
        if tr == "exact" and not (isinstance(rs.get("count"), int) and rs["count"] >= 0): add("error", f"resource {rid}", f"exact count {rs.get('count')!r}")
        elif tr == "usage_die" and rs.get("usage_die") not in ("d12", "d10", "d8", "d6", "d4", "empty"): add("error", f"resource {rid}", f"usage_die {rs.get('usage_die')!r}")
        elif tr not in ("exact", "usage_die"): add("error", f"resource {rid}", f"tracking {tr!r}")
    for inj in c.get("injuries") or []:
        if not (isinstance(inj, dict) and inj.get("home") in rules.INJURY_HOMES and inj.get("effect")):
            add("error", "injuries", f"injury needs injury/home/effect: {inj}")
    if mods.get("flexible_item_entitlement"):
        ip = p.get("item_points")
        if not isinstance(ip, int) or ip < 0: add("error", "item_points", f"{ip!r}: needs an integer >= 0 while module D is on")
    elif "item_points" in p: add("warn", "item_points", "saved while flexible_item_entitlement is off")
    # ---- records ----------------------------------------------------------------------------------
    pend, camp.pending = camp.pending, []          # import repairs wait for the next block; they are not stamped yet
    camp._view_cache.clear()
    recs = camp.records()
    camp.pending = pend
    camp._view_cache.clear()
    rnd = int(r.get("saved_completed_round") or 0)
    for rid, txt in recs.items():
        mm = re.match(r"^R(\d+):", txt)
        if mm and int(mm.group(1)) > rnd: add("error", f"record {rid}", f"stamped R{mm.group(1)} after the save round R{rnd}")
        if rid.split(".")[0] not in CAPSULE_OWNERS: add("warn", f"record {rid}", f"owner {rid.split('.')[0]!r} is not an engine owner (§6)")
        if rid == "player" or rid.startswith(("player.", "world_state.time", "world_state.location", "world_state.environment", "enabled_modules", "narrative_theme")):
            add("warn", f"record {rid}", "held by the readable save; capsule wins on load (older-save overlap)")
    for nid, n in (tree.get("npcs") or {}).items():
        if not isinstance(n, dict): continue
        miss = [k for k in ("name", "job", "belongs", "gender", "character") if k not in n]
        if miss: add("warn", f"npcs.{nid}", f"identity fields missing: {miss}")
        st, cap = n.get("state") or {}, n.get("capability") or {}
        if isinstance(st, dict) and "hp" in st and (cap.get("level") or cap.get("vitality") or cap.get("overall_level")):
            vv = rules.vitality_value({"capability": {**cap, "level": cap.get("level") or cap.get("overall_level")}}, True)
            size = cap.get("size", "normal")
            try:
                if int(st["hp"]) > rules.max_vitals(vv, size if size in rules.SIZES else "normal")["max_hp"]:
                    add("error", f"npcs.{nid}", f"state.hp {st['hp']} above derived max")
            except (ValueError, TypeError):
                add("warn", f"npcs.{nid}", f"state.hp {st['hp']!r} is not a number")
    for pid, pr in (tree.get("active_world_pressures") or {}).items():
        ck = (pr or {}).get("clock") if isinstance(pr, dict) else None
        if isinstance(ck, dict):
            try:
                if int(ck["filled"]) > int(ck["segments"]): add("error", f"pressure {pid}", f"filled {ck['filled']} > segments {ck['segments']}")
            except (KeyError, ValueError, TypeError):
                add("warn", f"pressure {pid}", "clock filled/segments not numeric")
    active_main = [q for q, v in (tree.get("quests") or {}).items() if isinstance(v, dict) and v.get("role") == "MAIN" and v.get("status") in ("available", "active", "blocked") and v.get("type") != "CHAIN"]
    chains = [q for q, v in (tree.get("quests") or {}).items() if isinstance(v, dict) and v.get("role") == "MAIN" and v.get("type") == "CHAIN" and v.get("status") in ("available", "active", "blocked")]
    if len(chains) > 1: add("warn", "quests", f"more than one non-terminal MAIN chain: {chains}")
    if numeric:
        for q, v in (tree.get("quests") or {}).items():
            if isinstance(v, dict) and v.get("status") in ("available", "active", "blocked") and v.get("type") in ("SHORT", "LONG") and v.get("quest_level") in (None, "") and not v.get("segments"):
                add("error", f"quests.{q}", "numeric_level_xp is on: a non-terminal quest needs quest_level")
    # ---- index references -----------------------------------------------------------------------------
    for sec, items in (rd.get("index") or {}).items():
        if isinstance(items, dict):
            for rid in items:
                if camp.get(f"{sec}.{rid}") is None: add("warn", "index", f"{sec}.{rid} is listed but no such record exists")
    return out


def report(findings: list[Finding]) -> str:
    n = {lv: sum(1 for f in findings if f.level == lv) for lv in ("error", "warn", "info")}
    head = f"audit: {n['error']} errors, {n['warn']} warnings, {n['info']} notes"
    return head + ("\n" + "\n".join(map(str, sorted(findings, key=lambda f: ("error", "warn", "info").index(f.level)))) if findings else "")


def check_chain(files: list, background_path: str) -> list[str]:
    """Validate saves oldest→newest: each alone, and each against the one before (every capsule record carried or retired)."""
    import re
    from pathlib import Path
    m = helper.mod()
    from .campaign import normalize_background, write_background
    import tempfile
    tmp = Path(tempfile.mkdtemp()) / "bg.md"
    write_background(tmp, normalize_background(Path(background_path).read_text(encoding="utf-8")))
    items = sorted(((int(re.search(r"_R(\d+)", Path(f).name).group(1)), Path(f)) for f in files))
    out, prev = [], None
    for n, f in items:
        v = m.do_validate(helper.ns(file=str(f), against=None, background=str(tmp)))
        line = f"R{n}: valid={v['valid']} records={v['decode']['records']}"
        if prev:
            w = m.do_validate(helper.ns(file=str(f), against=str(prev[1]), background=str(tmp)))
            sv = w["survival"]
            line += f" | vs R{prev[0]}: valid={w['valid']} dropped={len(sv['dropped'])}"
            if sv["dropped"]: line += f" {sv['dropped'][:3]}"
            if n - prev[0] > 10: line += f"  (gap: R{prev[0] + 10}..R{n - 10} missing)"
        out.append(line); prev = (n, f)
    return out
