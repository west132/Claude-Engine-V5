"""Campaign = BACKGROUND + readable state (Part A) + GM-Δ chain + journal.

Authority follows engine §4: the Ledger is `readable` (player block, time, place,
modules, theme, index) plus the capsule (every other record). The capsule is never
held a second time: its live view is always produced by the helper's own `merge`
over (previous save + this chat's GM-Δ chain), exactly as a save would build it.
"""
from __future__ import annotations
import copy
import datetime as _dt
import json
import os
import re
import shutil
from dataclasses import dataclass, field, asdict
from pathlib import Path

import yaml

from . import helper, rules, timeutil
from .config import Config

CAPSULE_OWNERS = {"world_state", "locations", "rights_obligations", "active_commitments",
                  "quests", "development_threads", "trackers", "npcs", "factions",
                  "active_world_pressures", "locked_case_truths", "open_suspicions",
                  "pending_payoffs", "unresolved_consequences", "ending_conditions",
                  "continuity_status"}
PLAYER_KEYS = ("identity", "archetype", "job", "belongs", "gender", "character", "status",
               "skills", "traits", "expertise", "growth_period", "progression", "vitality",
               "condition", "equipment", "money", "resources", "routines", "fighting_style",
               "knowledge")
INDEX_SECTIONS = ("npcs", "factions", "locations", "quests", "development_threads", "trackers",
                  "rights_obligations", "active_world_pressures")
MODULES = ("numeric_level_xp", "equipment_power_tiers", "bounded_scenario_endings",
           "flexible_item_entitlement")


class CampaignError(Exception):
    pass


@dataclass
class Entry:
    op: str                    # + ~ -
    id: str
    content: str
    hidden: bool = True        # display only: whether the player has seen the fact
    secret_terms: list[str] = field(default_factory=list)

    def plain_line(self) -> str:
        return f"{self.op} {self.id} :: {self.content}"


@dataclass
class Block:
    round: int
    prev: int
    entries: list[Entry] = field(default_factory=list)

    def render(self, encoding: str = "plain") -> str:
        head = f"GM-Δ {self.round} ⟵ {self.prev}"
        if not self.entries:
            return f"GM-Δ {self.round} none"
        out = [head]
        enc = helper.mod()._encode_text
        for e in self.entries:
            c = e.content
            if encoding != "plain":
                entry, n = enc(c, encoding)
                c = f"enc:{encoding} {entry}" + (f" · {n}" if encoding == "b64" else "")
            out.append(f"  {e.op} {e.id} :: {c}")
        return "\n".join(out)


# ---------------------------------------------------------------------------------------
def _plain(v):
    """YAML-loaded value with dates turned into ISO strings (dates are strings in saves)."""
    if isinstance(v, dict): return {str(k): _plain(x) for k, x in v.items()}
    if isinstance(v, list): return [_plain(x) for x in v]
    if isinstance(v, (_dt.date, _dt.datetime)): return v.isoformat()
    return v


def _merge(dst: dict, src: dict):
    for k, v in src.items():
        if isinstance(v, dict) and isinstance(dst.get(k), dict):
            _merge(dst[k], v)
        else:
            dst[k] = v


def normalize_background(text: str) -> dict:
    """A filled BACKGROUND_TEMPLATE has many ```yaml blocks; the helper reads one. Merge them.
    A block that starts indented continues the `player:` mapping (as in the template)."""
    blocks = re.findall(r"```ya?ml\n(.*?)```", text, re.S)
    if not blocks:
        blocks = [text]
    tree: dict = {}
    for b in blocks:
        lines = [l for l in b.splitlines() if l.strip() and not l.lstrip().startswith("#")]
        if not lines:
            continue
        indented = lines[0][0] in " \t"
        try:
            data = yaml.safe_load(b)
        except yaml.YAMLError as e:
            raise CampaignError(f"BACKGROUND YAML will not parse: {e}")
        if not isinstance(data, dict):
            continue
        if indented:
            tree.setdefault("player", {})
            _merge(tree["player"], _plain(data))
        else:
            _merge(tree, _plain(data))
    if not tree.get("background_id"):
        raise CampaignError("BACKGROUND needs a background_id (engine BACKGROUND_TEMPLATE §0)")
    return tree


def write_background(path: Path, tree: dict):
    body = yaml.safe_dump(tree, sort_keys=False, allow_unicode=True, width=100)
    path.write_text(f"# BACKGROUND — {tree['background_id']}\n\n```yaml\n{body}```\n", encoding="utf-8")


def _blank(v) -> bool:
    return v is None or v == "" or v == [] or v == {}


def _clean(v):
    """Drop template placeholders (None/empty) so saves carry only real values."""
    if isinstance(v, dict):
        return {k: _clean(x) for k, x in v.items() if not _blank(x) or isinstance(x, (list, dict))}
    if isinstance(v, list):
        return [_clean(x) for x in v]
    return v


def initial_readable(bg: dict, language: str, profile: str) -> dict:
    """Engine §16.2 steps 2-4: import the player's start, derive vitals, modules, theme."""
    mods = {m: False for m in MODULES}
    mods.update({k: bool(v) for k, v in (bg.get("enabled_modules") or {}).items() if k in mods})
    bp = bg.get("player") or {}
    player = {k: copy.deepcopy(bp[k]) for k in PLAYER_KEYS if k in bp and not _blank(bp[k])}
    for k in ("skills", "equipment", "resources", "routines", "fighting_style", "traits", "belongs"):
        player.setdefault(k, {} if k in ("skills", "resources", "routines") else [])
    for sid, sk in player["skills"].items():
        sk = player["skills"][sid] = sk or {}
        sk.setdefault("class", "NORMAL"); sk.setdefault("tier", "T1")
        sk.setdefault("growth_evidence", 0); sk.setdefault("ceiling_evidence", 0)
    wt = copy.deepcopy((bg.get("world_state") or {}).get("time") or {})
    wt.setdefault("day_index", 0)
    if wt.get("clock_minutes") in (None, ""):
        wt["clock_minutes"], wt["precision"] = 480, wt.get("precision") or "daypart"
    wt["clock_minutes"] = int(wt["clock_minutes"])
    wt["daypart"] = wt.get("daypart") or timeutil.daypart(wt["clock_minutes"])
    wt.setdefault("precision", "exact")
    wt.setdefault("season", "")
    wt["date"] = wt.get("date") or None
    player["growth_period"] = player.get("growth_period") or {"opened": wt["day_index"], "credited": []}
    player["growth_period"].setdefault("credited", [])
    if mods["numeric_level_xp"]:
        prog = player.setdefault("progression", {"system": "numeric_level_xp", "state": {"level": 1, "xp": 0}})
        prog.setdefault("system", "numeric_level_xp")
        prog.setdefault("state", {"level": 1, "xp": 0})
        player.pop("vitality", None)
    else:
        player.pop("progression", None)
        player.setdefault("vitality", "ordinary")
    if mods["flexible_item_entitlement"]:
        player["item_points"] = int(((bp.get("starting_item_points") or {}).get("points")) or 0)
    cond = player.setdefault("condition", {})
    v = rules.vitality_value(player, mods["numeric_level_xp"])
    draws = ((bg.get("setting_anchors") or {}).get("mp_powers") or {}).get("draws_mp") or []
    tier = rules.mp_tier(player, draws)
    mx = rules.max_vitals(v, "normal", tier)
    if cond.get("hp") in (None, ""): cond["hp"] = mx["max_hp"]
    if tier and cond.get("mp") in (None, ""): cond["mp"] = mx["max_mp"]
    cond.setdefault("injuries", [])
    cond.setdefault("fatigue", "none")
    ws = bg.get("world_state") or {}
    loc = ws.get("location")
    if isinstance(loc, dict): loc = loc.get("id") or loc.get("name")
    theme = copy.deepcopy(bg.get("narrative_theme") or {})
    theme.setdefault("initial", {}); theme.setdefault("current", copy.deepcopy(theme["initial"]))
    rd = {
        "background_ref": {"id": bg["background_id"]},
        "language": language, "profile": profile,
        "round": {"last_completed_round": 0, "saved_completed_round": 0},
        "world_state": {"location": loc or "unknown", "time": wt,
                        "environment": copy.deepcopy(ws.get("environment") or {})},
        "player": _clean(player),
        "enabled_modules": mods,
        "narrative_theme": theme,
        "index": {**{s: {} for s in INDEX_SECTIONS}, "pending_payoffs": []},
    }
    rd["player"].setdefault("condition", {}).setdefault("injuries", [])
    return rd


def default_session(encoding: str = "plain") -> dict:
    return {"encoding": encoding, "combat": {}, "plan": "", "pending_odds": None, "dues": [],
            "must_settle": [], "ended": False, "history": [], "seq": 0}


# ---------------------------------------------------------------------------------------
class Campaign:
    def __init__(self, cfg: Config, name: str):
        self.cfg, self.name = cfg, name
        self.dir = cfg.campaigns_dir / name
        self.work, self.saves = self.dir / "work", self.dir / "saves"
        self.bg_path = self.dir / "background.md"
        self.bg: dict = {}
        self.readable: dict = {}
        self.closed_readable: dict = {}
        self.session: dict = default_session()
        self.pending: list[Entry] = []          # entries from rounds-less turns, joining the next block
        self.blocks: list[Block] = []           # GM-Δ chain since the newest save
        self.base_save: Path | None = None
        self._view_cache: dict = {}

    # ---- creation / opening -----------------------------------------------------------
    @classmethod
    def create(cls, cfg: Config, name: str, background_text: str, language: str | None = None,
               profile: str | None = None, encoding: str | None = None, fill: dict | None = None) -> "Campaign":
        if not re.fullmatch(r"[A-Za-z0-9_\-]{1,40}", name):
            raise CampaignError("campaign name: letters, digits, _ and - only (max 40)")
        c = cls(cfg, name)
        if c.dir.exists():
            raise CampaignError(f"campaign {name!r} already exists")
        helper.load(cfg.engine_dir)
        tree = normalize_background(background_text)
        from . import bgen
        if fill is not None or bgen.unassigned(tree):
            bgen.apply_fill(tree, fill or {})            # the player sets every [UNASSIGNED] before Round 1
        c.work.mkdir(parents=True); c.saves.mkdir()
        (c.dir / "background.source.md").write_text(background_text, encoding="utf-8")
        write_background(c.bg_path, tree)
        c.bg = tree
        c.readable = initial_readable(tree, language or cfg.game.language, profile or cfg.game.profile)
        c.closed_readable = copy.deepcopy(c.readable)
        c.session = default_session(encoding or cfg.game.encoding)
        c.write_journal()
        return c

    @classmethod
    def open(cls, cfg: Config, name: str) -> "Campaign":
        c = cls(cfg, name)
        if not c.dir.exists():
            raise CampaignError(f"no campaign {name!r}")
        helper.load(cfg.engine_dir)
        c.bg = helper.mod()._bg_tree(c.bg_path)
        j = json.loads((c.work / "journal.json").read_text(encoding="utf-8"))
        c.readable, c.closed_readable = j["readable"], j["closed_readable"]
        c.session = {**default_session(), **j["session"]}
        c.pending = [Entry(**e) for e in j.get("pending", [])]
        c.blocks = [Block(b["round"], b["prev"], [Entry(**e) for e in b["entries"]]) for b in j["blocks"]]
        c.base_save = (c.saves / j["base_save"]) if j.get("base_save") else None
        return c

    # ---- journal -------------------------------------------------------------------------
    def write_journal(self):
        j = {"readable": self.readable, "closed_readable": self.closed_readable,
             "session": {**self.session, "history": self.session["history"][-40:]},
             "pending": [asdict(e) for e in self.pending],
             "blocks": [{"round": b.round, "prev": b.prev, "entries": [asdict(e) for e in b.entries]}
                        for b in self.blocks],
             "base_save": self.base_save.name if self.base_save else None}
        tmp = self.work / "journal.json.tmp"
        tmp.write_text(json.dumps(j, ensure_ascii=False, indent=1), encoding="utf-8")
        os.replace(tmp, self.work / "journal.json")
        (self.work / "chain.md").write_text(self.chain_text(), encoding="utf-8")

    def snapshot(self):
        return copy.deepcopy((self.readable, self.session, self.pending))

    def restore(self, snap):
        self.readable, self.session, self.pending = copy.deepcopy(snap)
        self._view_cache.clear()

    # ---- convenient accessors ---------------------------------------------------------
    @property
    def player(self) -> dict: return self.readable["player"]
    @property
    def time(self) -> dict: return self.readable["world_state"]["time"]
    @property
    def modules(self) -> dict: return self.readable["enabled_modules"]
    @property
    def numeric(self) -> bool: return bool(self.modules.get("numeric_level_xp"))
    @property
    def rnd(self) -> int: return int(self.readable["round"]["last_completed_round"])
    @property
    def S(self) -> int: return int(self.readable["round"]["saved_completed_round"])
    @property
    def T(self) -> int: return (self.S // 10 + 1) * 10
    @property
    def language(self) -> str: return self.readable.get("language", "en")
    @property
    def profile(self) -> str: return self.readable.get("profile", "full")
    @property
    def encoding(self) -> str: return self.session.get("encoding", "plain")

    def last_delta_round(self) -> int:
        return self.blocks[-1].round if self.blocks else self.S

    # ---- chain -------------------------------------------------------------------------
    def chain_text(self, extra: Block | None = None) -> str:
        blocks = self.blocks + ([extra] if extra else [])
        return "\n\n".join(b.render(self.encoding) for b in blocks) + ("\n" if blocks else "")

    def make_block(self, round_no: int, entries: list[Entry]) -> Block:
        return Block(round_no, self.last_delta_round(), list(self.pending) + list(entries))

    def commit_block(self, block: Block):
        self.blocks.append(block)
        self.pending = []
        self._view_cache.clear()

    # ---- live capsule view (always the helper's own merge) ----------------------------
    def _merge_view(self, extra: Block | None):
        key = (len(self.blocks), extra.render("plain") if extra else "", len(self.pending))
        if key in self._view_cache:
            return self._view_cache[key]
        m = helper.mod()
        records: dict[str, str] = {}
        retired: list[tuple[str, str]] = []
        extra_all = extra
        if self.pending and extra is None:
            extra_all = Block(self.last_delta_round() + 1, self.last_delta_round(), list(self.pending))
        elif self.pending and extra is not None:
            extra_all = Block(extra.round, extra.prev, list(self.pending) + list(extra.entries))
        chain = self.chain_text(extra_all)
        tmp = self.work / "tmp"
        tmp.mkdir(exist_ok=True)
        if chain.strip():
            (tmp / "chain.md").write_text(chain, encoding="utf-8")
            out = m.do_merge(helper.ns(base=str(self.base_save) if self.base_save else None,
                                       background=str(self.bg_path), deltas=str(tmp / "chain.md"),
                                       out=None, save_round=None, encoding="plain"))
            (tmp / "cap.md").write_text(out["capsule_yaml"], encoding="utf-8")
            caps, ret = m._capsule_records(str(tmp / "cap.md"))
            warn = out.get("warnings")
            degraded = out.get("degraded")
        elif self.base_save:
            caps, ret = m._capsule_records(str(self.base_save))
            warn = degraded = None
        else:
            caps, ret, warn, degraded = [], [], None, None
        for r in caps:
            t = m._text_of(r)
            records[r["id"]] = t if t is not None else "degraded: undecodable"
        retired = [(r["id"], r["reason"] or "") for r in ret]
        res = (records, retired, warn, degraded)
        self._view_cache = {key: res}
        return res

    def records(self, extra: Block | None = None) -> dict[str, str]:
        return self._merge_view(extra)[0]

    def merge_notes(self, extra: Block | None = None):
        r = self._merge_view(extra)
        return r[2], r[3]

    def tree(self, extra: Block | None = None) -> dict:
        """BACKGROUND records overlaid with the capsule: the Ledger as the model should see it."""
        records, retired, _, _ = self._merge_view(extra)
        t = copy.deepcopy({k: v for k, v in self.bg.items() if k in CAPSULE_OWNERS})
        for rid, _why in retired:
            _del_path(t, rid)
        for rid in sorted(records, key=lambda r: r.count(".")):
            text = re.sub(r"^R\d+:\s*", "", records[rid])
            if text.startswith("no longer holds"):
                _del_path(t, rid)
            else:
                _set_path(t, rid, _parse_value(text))
        return t

    def get(self, path: str, extra: Block | None = None):
        node = self.tree(extra)
        for part in path.split("."):
            if isinstance(node, dict) and part in node: node = node[part]
            elif isinstance(node, list) and re.fullmatch(r"r0_(\d+)", part) and 0 < int(part[3:]) <= len(node):
                node = node[int(part[3:]) - 1]
            else:
                return None
        return node

    def location_name(self) -> str:
        loc = self.readable["world_state"]["location"]
        rec = self.get(f"locations.{loc}")
        return (rec or {}).get("name", loc) if isinstance(rec, dict) else str(loc)

    def glossary(self) -> dict:
        g = (self.get("world_state.glossary") or {})
        return g.get(self.language, {}) if isinstance(g, dict) else {}


def _parse_value(text: str):
    if " | R" in text and re.search(r"\| R\d+:", text):
        return text
    s = text.strip()
    if s[:1] in "{[\"" and s:
        try: return json.loads(s)
        except Exception: pass
    if s in ("true", "false"): return s == "true"
    if re.fullmatch(r"-?\d+", s): return int(s)
    return text


def _set_path(tree: dict, path: str, value):
    parts = path.split(".")
    node = tree
    for i, p in enumerate(parts[:-1]):
        nxt = None
        if isinstance(node, list):
            m = re.fullmatch(r"r0_(\d+)", p)
            if not (m and 0 < int(m.group(1)) <= len(node)): return
            node = node[int(m.group(1)) - 1]; continue
        if p not in node or not isinstance(node[p], (dict, list)):
            node[p] = {}
        elif isinstance(node[p], list) and not re.fullmatch(r"r0_\d+", parts[i + 1]):
            # a list in BACKGROUND (e.g. material_history) gains a keyed record: keep its items as r0_N
            node[p] = {f"r0_{n + 1}": x for n, x in enumerate(node[p])}
        node = node[p]
    last = parts[-1]
    if isinstance(node, list) and not re.fullmatch(r"r0_\d+", last):
        return
    if isinstance(node, list):
        m = re.fullmatch(r"r0_(\d+)", last)
        if m and 0 < int(m.group(1)) <= len(node): node[int(m.group(1)) - 1] = value
    else:
        node[last] = value


def _del_path(tree: dict, path: str):
    parts = path.split(".")
    node = tree
    for p in parts[:-1]:
        if isinstance(node, dict) and p in node: node = node[p]
        else: return
    if isinstance(node, dict): node.pop(parts[-1], None)
