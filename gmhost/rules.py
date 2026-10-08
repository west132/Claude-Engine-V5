"""Engine tables and derived values as code (engine §10.5, §11, §A). No judgement here."""
from __future__ import annotations
import re

from . import helper

VITALITY = {"ordinary": 1, "seasoned": 3, "veteran": 5, "exceptional": 8, "heroic": 11, "legendary": 20}
TIER_BONUS = {"T1": 1, "T2": 2, "T3": 3, "T4": 4}
TIER_ORDER = ["T1", "T2", "T3", "T4"]
CEILING = {"NORMAL": "T2", "ELITE": "T3", "LEGENDARY": "T4"}
SIZES = ("small", "normal", "large", "huge")

# §10.5 DAMAGE: what hits sets the dice, never the result.
DAMAGE = {
    "weapon": {"unarmed": "1d3", "light": "1d6", "one_handed": "1d8", "two_handed": "2d6", "bow": "1d8"},
    "creature": {"small": "1d4", "man_sized": "1d6", "large": "2d6", "huge": "3d6"},
    "hazard": {"light": "1d6", "serious": "2d6", "grave": "4d6"},
    "power": {"T1": "1d8", "T2": "2d6", "T3": "3d6", "T4": "4d6"},
}
SOAK = {"none": 0, "light": 1, "heavy": 2}
INJURY_HOMES = ("capability", "feasibility", "environment", "time", "sensory", "position", "simultaneous")
CONDITION_CATS = ("environment", "time", "sensory", "position", "simultaneous")
HEAL_DEFAULT = {"minor": "2d6", "standard": "4d6", "strong": "full"}


def damage_dice(kind: str, size: str) -> str:
    try:
        return DAMAGE[kind][size]
    except KeyError:
        opts = {k: list(v) for k, v in DAMAGE.items()}
        raise ValueError(f"unknown damage source {kind}/{size}; engine §10.5 allows {opts}")


def vitality_value(player_or_actor: dict, numeric: bool) -> int:
    if numeric:
        prog = (player_or_actor.get("progression") or {}).get("state") or {}
        if prog.get("level"):
            return int(prog["level"])
    cap = player_or_actor.get("vitality") or (player_or_actor.get("capability") or {}).get("vitality")
    if isinstance(cap, str) and cap in VITALITY:
        return VITALITY[cap]
    lvl = (player_or_actor.get("capability") or {}).get("level")
    if isinstance(lvl, int):
        return lvl
    return 1


def mp_tier(actor: dict, draws_mp: list[str]) -> str | None:
    best = None
    for sid, sk in (actor.get("skills") or {}).items():
        if sid in draws_mp or any(str(d).lower() in str(sid).lower() for d in draws_mp):
            t = (sk or {}).get("tier")
            if t in TIER_ORDER and (best is None or TIER_ORDER.index(t) > TIER_ORDER.index(best)):
                best = t
    return best


def max_vitals(v: int, size: str = "normal", tier: str | None = None) -> dict:
    return helper.mod().do_vitals(helper.ns(v=v, size=size, mp_tier=tier))


def parse_dice(spec: str) -> tuple[int, int]:
    m = re.fullmatch(r"(\d+)d(\d+)", spec.strip().lower())
    if not m:
        raise ValueError(f"bad dice {spec!r}")
    return int(m.group(1)), int(m.group(2))


def personal_skill_level(level: int | None, tier: str) -> int | None:
    return None if level is None else level + TIER_BONUS[tier]


def odds_percent(capmod: int, tool: int, difficulty: int) -> int:
    need = difficulty - capmod - tool
    return sum(1 for x in range(1, 11) for y in range(1, 11) if x + y >= need)
