"""Per-turn working context shared by all tools."""
from __future__ import annotations
import re
from dataclasses import dataclass, field

from . import helper, rules, timeutil
from .campaign import Campaign, Entry, Block


class ToolError(Exception):
    """A tool call the host refuses. The message goes back to the model verbatim."""


@dataclass
class TurnCtx:
    camp: Campaign
    player_text: str = ""
    lines: list[str] = field(default_factory=list)       # engine lines, in order, shown verbatim
    status: list[str] = field(default_factory=list)      # host-computed status changes shown to the player
    log: list[str] = field(default_factory=list)         # engine-side notes (growth evidence etc.)
    entries: list[Entry] = field(default_factory=list)
    must_settle: dict = field(default_factory=dict)
    closed: dict | None = None
    stopped_for_odds: bool = False
    secret_terms: set = field(default_factory=set)
    learned: list[str] = field(default_factory=list)     # quiet noticed changes (tier raises etc.)
    rolled: bool = False
    opened_cards: set = field(default_factory=set)
    engine: object = None
    pending_at_start: object = None

    # ---- ledger views including this turn's uncommitted entries --------------------
    def preview(self) -> Block:
        c = self.camp
        return Block(c.rnd + 1, c.last_delta_round(), list(self.entries))

    def tree(self) -> dict:
        return self.camp.tree(self.preview() if self.entries else None)

    def get(self, path: str):
        node = self.tree()
        for part in path.split("."):
            if isinstance(node, dict) and part in node: node = node[part]
            elif isinstance(node, list) and re.fullmatch(r"r0_(\d+)", part) and 0 < int(part[3:]) <= len(node):
                node = node[int(part[3:]) - 1]
            else:
                return None
        return node

    def add_entry(self, op: str, rid: str, content, hidden: bool = True, secret=None):
        text = content if isinstance(content, str) else __import__("json").dumps(content, ensure_ascii=False)
        self.entries.append(Entry(op, rid, re.sub(r"\s+", " ", text).strip(), hidden, list(secret or [])))
        self.camp._view_cache.clear()

    def settle(self, prefix: str):
        for k in [k for k in self.must_settle if k.startswith(prefix)]:
            del self.must_settle[k]


# ---- actors that can be hurt ----------------------------------------------------------
class Hurtable:
    """Uniform view of anything with HP: the player, a registered combatant, or a recorded NPC."""

    def __init__(self, ctx: TurnCtx, actor_id: str):
        self.ctx, self.id = ctx, actor_id
        camp = ctx.camp
        combat = camp.session["combat"]
        if actor_id == "player":
            self.kind, self.name = "player", camp.player.get("identity", {}).get("name", "player")
            v = rules.vitality_value(camp.player, camp.numeric)
            draws = ((camp.bg.get("setting_anchors") or {}).get("mp_powers") or {}).get("draws_mp") or []
            self.tier = rules.mp_tier(camp.player, draws)
            self.max_hp = rules.max_vitals(v, "normal", self.tier)["max_hp"]
            self.max_mp = rules.max_vitals(v, "normal", self.tier).get("max_mp")
        elif actor_id in combat:
            self.kind, a = "combat", combat[actor_id]
            self.name, self.max_hp, self.max_mp, self.tier = a["name"], a["max_hp"], None, None
        else:
            npc = ctx.get(f"npcs.{actor_id}")
            if not isinstance(npc, dict):
                raise ToolError(f"unknown actor {actor_id!r}: use 'player', a registered combatant "
                                "(combat add), or a recorded npc id")
            cap = npc.get("capability") or {}
            if not (cap.get("level") or cap.get("vitality")):
                raise ToolError(f"npcs.{actor_id} has no committed level or vitality; commit "
                                f"`~ npcs.{actor_id}.capability.vitality` (or level) first (I3)")
            v = rules.vitality_value({"capability": cap}, True)
            self.kind, self.name = "npc", npc.get("name", actor_id)
            self.max_hp = rules.max_vitals(v, cap.get("size", "normal"))["max_hp"]
            self.max_mp = self.tier = None

    # hp ----------------------------------------------------------------------------------
    @property
    def hp(self) -> int:
        if self.kind == "player": return int(self.ctx.camp.player["condition"]["hp"])
        if self.kind == "combat": return int(self.ctx.camp.session["combat"][self.id]["hp"])
        st = (self.ctx.get(f"npcs.{self.id}.state") or {})
        return rules.lead_int(st.get("hp"), self.max_hp) if isinstance(st, dict) else self.max_hp

    def set_hp(self, v: int):
        v = max(0, min(self.max_hp, int(v)))
        if self.kind == "player": self.ctx.camp.player["condition"]["hp"] = v
        elif self.kind == "combat": self.ctx.camp.session["combat"][self.id]["hp"] = v
        else: self.ctx.add_entry("~", f"npcs.{self.id}.state.hp", str(v), hidden=False)

    @property
    def mp(self):
        return self.ctx.camp.player["condition"].get("mp") if self.kind == "player" else None

    def set_mp(self, v: int):
        if self.kind == "player": self.ctx.camp.player["condition"]["mp"] = max(0, int(v))

    @property
    def soak(self) -> int:
        camp = self.ctx.camp
        if self.kind == "player":
            best = 0
            for it in camp.player.get("equipment") or []:
                props = " ".join(map(str, it.get("special_properties") or [])) + " " + str(it.get("type", ""))
                if it.get("condition") == "critical":
                    continue
                if "heavy armour" in props.lower() or "heavy armor" in props.lower(): best = max(best, 2)
                elif "light armour" in props.lower() or "light armor" in props.lower(): best = max(best, 1)
            return best
        if self.kind == "combat":
            return int(camp.session["combat"][self.id].get("soak", 0))
        return 0
