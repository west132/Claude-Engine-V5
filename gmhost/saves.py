"""Saving and loading (engine §16, SAVE_TEMPLATE). Code writes Part A, the helper builds Part B."""
from __future__ import annotations
import copy
import re
import shutil
from pathlib import Path

import yaml

from . import helper
from .campaign import Campaign, CampaignError, Entry, Block, _plain, default_session, normalize_background, write_background


class SaveFailure(Exception):
    def __init__(self, msg, detail=None):
        super().__init__(msg)
        self.detail = detail


def _dump(d: dict) -> str:
    return yaml.safe_dump(d, sort_keys=False, allow_unicode=True, width=100, default_flow_style=False)


def _strip_nulls(player: dict) -> dict:
    """The lint rejects `usage_die: null`; keep keys only where they mean something."""
    p = copy.deepcopy(player)
    for rid, r in (p.get("resources") or {}).items():
        if isinstance(r, dict):
            if r.get("tracking") != "usage_die": r.pop("usage_die", None)
            if r.get("tracking") != "exact": r.pop("count", None)
    return p


def part_a(camp: Campaign, readable: dict, save_round: int) -> str:
    r = readable
    rnd = {"last_completed_round": save_round, "saved_completed_round": save_round}
    parts = [
        f"# SAVE — {camp.name} — R{save_round}\n",
        "Written by the GM host. Part A is what the player knows; Part B (the capsule) holds every other record.\n",
        "## 1. Current state\n",
        # flow style on purpose: the helper's scanner reads a line starting `id:` as a capsule record
        "```yaml\n" + f"background_ref: {{id: {r['background_ref']['id']}}}\n" +
        _dump({"language": r["language"], "profile": r["profile"], "round": rnd,
               "world_state": r["world_state"]}) + "```\n",
        "## 2. Player\n",
        "```yaml\n" + _dump({"player": _strip_nulls(r["player"])}) + "```\n",
        "## 3. Modules and theme\n",
        "```yaml\n" + _dump({"enabled_modules": r["enabled_modules"],
                             "narrative_theme": r["narrative_theme"]}) + "```\n",
        "## 4. Index\n",
        "```yaml\n" + _dump({"index": r["index"]}) + "```\n",
    ]
    return "\n".join(parts)


def build_save(camp: Campaign) -> dict:
    """Engine §16.1 EXPORTED procedure, run by code. Raises SaveFailure; otherwise the file is delivered."""
    m = helper.mod()
    n = camp.rnd
    if n == camp.S and camp.base_save is not None:
        return {"path": str(camp.base_save), "round": n, "already": True, "valid": True}
    tmp = camp.work / "tmp"
    tmp.mkdir(exist_ok=True)
    chain = tmp / "save_chain.md"
    chain.write_text(camp.chain_text(), encoding="utf-8")
    enc = camp.encoding
    if camp.blocks:
        out = m.do_merge(helper.ns(base=str(camp.base_save) if camp.base_save else None,
                                   background=str(camp.bg_path), deltas=str(chain), out=None,
                                   save_round=n, encoding=enc))
        capsule = out["capsule_yaml"]
        merge_info = {k: out[k] for k in ("warnings", "gaps", "degraded", "replays") if k in out}
    elif camp.base_save is None:
        capsule = m._capsule_yaml([], [], enc, n, None, camp.bg.get("background_id"))
        merge_info = {}
    else:
        raise SaveFailure("nothing new to fold into a save")
    readable = copy.deepcopy(camp.closed_readable)
    readable["round"] = {"last_completed_round": n, "saved_completed_round": n}
    a = part_a(camp, readable, n)
    if re.search(r"^\s*-?\s*id:", a, re.M):
        raise SaveFailure("Part A would contain a line starting `id:`, which the helper reads as a capsule record")
    text = a + "\n# PART B — CAPSULE\n\n```yaml\n" + capsule + "```\n"
    cand = tmp / "candidate_save.md"
    cand.write_text(text, encoding="utf-8")
    against = None                       # the helper cannot compare against a capsule with no records
    if camp.base_save is not None and m._capsule_records(str(camp.base_save))[0]:
        against = str(camp.base_save)
    v = m.do_validate(helper.ns(file=str(cand), against=against, background=str(camp.bg_path)))
    if not v.get("valid"):
        raise SaveFailure("validate reported problems", v)
    dest = camp.saves / f"save_{camp.name}_R{n}.md"
    shutil.move(str(cand), dest)
    arch = camp.work / "archive"
    arch.mkdir(exist_ok=True)
    shutil.copy(chain, arch / f"chain_to_R{n}.md")
    camp.base_save = dest
    camp.blocks = []
    camp.readable["round"]["saved_completed_round"] = n
    camp.closed_readable["round"]["saved_completed_round"] = n
    camp.session["dues"] = _dues_list(v.get("dues") or {})
    camp._view_cache.clear()
    camp.write_journal()
    return {"path": str(dest), "round": n, "valid": True, "merge": merge_info,
            "dues": camp.session["dues"], "audit": v.get("dues", {}).get("audit")}


def _dues_list(d: dict) -> list[str]:
    out = []
    for k in ("overdue", "unregistered_trigger", "clock_without_due", "actors_without_plan",
              "incidental_but_referenced", "open_past_all_dates", "work_without_quest", "unread_date"):
        for item in d.get(k) or []:
            out.append(f"{k}: {item}")
    aud = d.get("audit")
    if isinstance(aud, dict):
        for item in aud.get("stale") or []:
            out.append(f"audit: {item}")
    return out


# ---- loading --------------------------------------------------------------------------
def parse_part_a(text: str) -> dict:
    cut = re.search(r"^\s*(?:#\s*PART B|capsule:\s*$)", text, re.M)
    head = text[:cut.start()] if cut else text
    out: dict = {}
    for b in re.findall(r"```ya?ml\n(.*?)```", head, re.S):
        d = yaml.safe_load(b)
        if isinstance(d, dict):
            out.update(_plain(d))
    return out


def import_save(cfg, name: str, save_text: str, background_text: str) -> Campaign:
    """Start (or restore) a campaign from a save file plus the BACKGROUND it points at (engine §16.5)."""
    helper.load(cfg.engine_dir)
    m = helper.mod()
    readable = parse_part_a(save_text)
    for k in ("background_ref", "world_state", "player", "round"):
        if k not in readable:
            raise CampaignError(f"save is missing Part A field {k!r}")
    tree = normalize_background(background_text)
    want = readable["background_ref"].get("id")
    if want and want != tree["background_id"]:
        raise CampaignError(f"this save points at BACKGROUND {want!r}, got {tree['background_id']!r}")
    c = Campaign(cfg, name)
    if c.dir.exists():
        raise CampaignError(f"campaign {name!r} already exists")
    c.work.mkdir(parents=True); c.saves.mkdir()
    write_background(c.bg_path, tree)
    (c.dir / "background.source.md").write_text(background_text, encoding="utf-8")
    n = int(readable["round"].get("saved_completed_round") or readable["round"].get("last_completed_round") or 0)
    dest = c.saves / f"save_{name}_R{n}.md"
    dest.write_text(save_text, encoding="utf-8")
    v = m.do_validate(helper.ns(file=str(dest), against=None, background=str(c.bg_path)))
    if not v.get("valid"):
        shutil.rmtree(c.dir)
        raise CampaignError("the save does not validate: " + str({k: v[k] for k in v if k in ("decode", "capsule", "lint", "background_mismatch", "delta_note")}))
    c.bg = tree
    # older saves omit fields the template now has: default them the way the engine does (profile full, English)
    readable.setdefault("language", "en")
    readable.setdefault("profile", "full")
    readable.setdefault("enabled_modules", {**{m: False for m in ("numeric_level_xp", "equipment_power_tiers", "bounded_scenario_endings", "flexible_item_entitlement")},
                                            **{k: bool(v) for k, v in (tree.get("enabled_modules") or {}).items()}})
    readable.setdefault("narrative_theme", tree.get("narrative_theme") or {"initial": {}, "current": {}})
    readable["index"] = {**{s: {} for s in ("npcs", "factions", "locations", "quests", "development_threads", "trackers",
                                          "rights_obligations", "active_world_pressures")}, "pending_payoffs": [],
                         **(readable.get("index") or {})}
    readable["round"] = {"last_completed_round": n, "saved_completed_round": n}
    c.readable, c.closed_readable = readable, copy.deepcopy(readable)
    c.session = default_session()
    c.session["dues"] = _dues_list(v.get("dues") or {})
    c.base_save = dest
    c.session["import_repairs"] = repair_import(c)
    c.write_journal()
    return c


_DATE_PREFIX = re.compile(r"\d{4}-\d{2}-\d{2}(?:[ T]\d{1,2}:\d{2})?|Year\s+\d+,\s*[A-Za-z][\w\-]*\s+\d+(?:,?\s+\d{1,2}:\d{2})?")
_IDENTITY = {"npcs": ("name", "job", "belongs", "gender", "character"), "factions": ("name", "role")}


def repair_import(c: Campaign) -> list[str]:
    """Make an older/chat-written save obey the engine's field rules, honestly (I12): values that carry prose
    where a number or date belongs are cut to the number/date; fields the engine requires but play never
    established become `unknown`; a lost reserve is restored from BACKGROUND and marked degraded.
    Changes to capsule records join the next GM-Δ block; every repair is listed so nothing is silent."""
    from .campaign import Entry
    from . import rules
    notes: list[str] = []
    p = c.player
    if c.modules.get("flexible_item_entitlement") and not isinstance(p.get("item_points"), int):
        start = int((((c.bg.get("player") or {}).get("starting_item_points")) or {}).get("points") or 0)
        p["item_points"] = start
        p.pop("starting_item_points", None)
        c.closed_readable["player"] = c.readable["player"]
        c.pending.append(Entry("+", "continuity_status.degraded.item_points_reserve",
                               f"item_points was not recorded in the imported save; restored from BACKGROUND starting value {start}", True))
        notes.append(f"item_points missing → restored to BACKGROUND's {start} (marked degraded)")
    tree = c.tree()
    def fix(rid, new, why):
        c.pending.append(Entry("~", rid, str(new), True)); notes.append(f"{rid}: {why}")
    for pid, pr in (tree.get("active_world_pressures") or {}).items():
        ck = (pr or {}).get("clock") if isinstance(pr, dict) else None
        if not isinstance(ck, dict): continue
        for f in ("filled", "segments"):
            v = ck.get(f)
            if not isinstance(v, int):
                n = rules.lead_int(v)
                if n is not None: fix(f"active_world_pressures.{pid}.clock.{f}", n, f"{f} held prose {str(v)[:40]!r} → {n}")
        due = ck.get("due")
        if isinstance(due, str):
            ms = _DATE_PREFIX.findall(due)
            if ms and due.strip() != ms[0].strip():
                fix(f"active_world_pressures.{pid}.clock.due", ms[0], f"due held prose after the date → {ms[0]!r}")
    for nid, n in (tree.get("npcs") or {}).items():
        if not isinstance(n, dict): continue
        st = n.get("state")
        if isinstance(st, dict) and "hp" in st and not isinstance(st["hp"], int):
            v = rules.lead_int(st["hp"])
            if v is not None: fix(f"npcs.{nid}.state.hp", v, f"hp held prose → {v}")
    for owner, req in _IDENTITY.items():
        for rid, rec in (tree.get(owner) or {}).items():
            if not isinstance(rec, dict): continue
            miss = [f for f in req if f not in rec]
            line = ((c.readable.get("index") or {}).get(owner) or {}).get(rid) or ""
            idx_name = line.split(" — ")[0].strip() if " — " in line else ""
            for f in miss:
                val = idx_name if (f == "name" and idx_name) else "unknown"
                c.pending.append(Entry("+", f"{owner}.{rid}.{f}", val, True))
            if miss: notes.append(f"{owner}.{rid}: required fields not established → unknown: {miss}")
    if notes:
        c._view_cache.clear()
    return notes
