"""Round-0 BACKGROUND: validate a filled BACKGROUND, or have the model fill the template from a premise."""
from __future__ import annotations
import re

import yaml

from . import rules
from .campaign import CampaignError, normalize_background, initial_readable
from .textutil import extract_json, strip_think

_SLUG = re.compile(r"^[a-z0-9][a-z0-9_\-]{2,60}$")


def problems(tree: dict) -> list[str]:
    p = []
    bid = tree.get("background_id")
    if not isinstance(bid, str) or not _SLUG.match(bid): p.append("background_id: a lowercase slug such as `salt_road_v1`")
    if tree.get("provenance") not in ("authored", "generated", "mixed"): p.append("provenance: authored | generated | mixed")
    st = tree.get("setting") or {}
    for k in ("world", "era", "starting_region", "mode"):
        if not st.get(k): p.append(f"setting.{k} is required")
    if st.get("mode") not in ("canon", "historical", "original", "alternate"): p.append("setting.mode: canon | historical | original | alternate")
    pl = tree.get("player") or {}
    if not (pl.get("identity") or {}).get("name"): p.append("player.identity.name is required")
    for k in ("archetype", "job", "gender", "character", "status"):
        if not pl.get(k): p.append(f"player.{k} is required (use `unknown` if the setting leaves it open)")
    for sid, sk in (pl.get("skills") or {}).items():
        sk = sk or {}
        if sk.get("class", "NORMAL") not in rules.CEILING: p.append(f"skill {sid}: class NORMAL|ELITE|LEGENDARY")
        if sk.get("tier", "T1") not in rules.TIER_ORDER: p.append(f"skill {sid}: tier T1..T4")
        elif sk.get("class", "NORMAL") in rules.CEILING and \
                rules.TIER_ORDER.index(sk.get("tier", "T1")) > rules.TIER_ORDER.index(rules.CEILING[sk.get("class", "NORMAL")]):
            p.append(f"skill {sid}: tier above its class ceiling")
    mods = tree.get("enabled_modules") or {}
    if mods.get("numeric_level_xp") and not ((pl.get("progression") or {}).get("state") or {}).get("level"):
        p.append("numeric_level_xp is on: player.progression.state.level is required")
    ws = tree.get("world_state") or {}
    loc = ws.get("location")
    if not loc: p.append("world_state.location is required")
    elif loc not in (tree.get("locations") or {}): p.append(f"world_state.location {loc!r} must be a key under locations")
    for nid, n in (tree.get("npcs") or {}).items():
        miss = [k for k in ("name", "job", "belongs", "gender", "character") if k not in (n or {})]
        if miss: p.append(f"npcs.{nid}: missing {miss} (use `unknown`)")
    for pid, pr in (tree.get("active_world_pressures") or {}).items():
        ck = (pr or {}).get("clock")
        if ck and not all(k in ck for k in ("name", "segments", "filled", "pace", "due", "on_fill")):
            p.append(f"pressure {pid}: clock needs name, segments, filled, pace, due, on_fill")
    return p


def check_background_text(text: str) -> dict:
    tree = normalize_background(text)
    errs = problems(tree)
    if errs:
        raise CampaignError("BACKGROUND problems:\n- " + "\n- ".join(errs))
    initial_readable(tree, "en", "full")      # must import without error
    return tree


GEN_SYSTEM = """ROLE: BACKGROUND_WRITER
You write the Round-0 BACKGROUND file for a text RPG, following the template below exactly. Output ONE ```yaml block containing every
section as a single YAML mapping (setting, setting_anchors, enabled_modules, player, locations, npcs, active_world_pressures, world_state,
narrative_theme, ...), starting with background_id, provenance: generated and requested. Fill in only what the game uses. Never grant unstated
capability, gear or connections. Keep names and facts coherent. Quote any string that contains a comma or colon. Dates use YYYY-MM-DD or the
setting's own calendar; every plan/clock `due` is a date the world can reach. world_state.location must be a key under locations.

======== BACKGROUND TEMPLATE (verbatim) ========
{template}
"""


def generate(backend, template_text: str, premise: str, language: str, numeric: bool, on_event=lambda e: None, tries: int = 3) -> str:
    sys = GEN_SYSTEM.format(template=template_text)
    req = (f"PREMISE FROM THE PLAYER:\n{premise}\n\nGame language for names and descriptions: {language}. "
           f"Module numeric_level_xp: {'ON (give the player a level)' if numeric else 'OFF (give a vitality band)'}. "
           "Record the player's wishes under `requested`. Output the YAML block only.")
    msgs = [{"role": "system", "content": sys}, {"role": "user", "content": req}]
    last = ""
    for i in range(tries):
        on_event({"type": "phase", "text": f"writing the background (attempt {i + 1})"})
        raw = strip_think(backend.chat(msgs, temperature=0.7, max_tokens=6000))
        m = re.search(r"```ya?ml\n(.*?)```", raw, re.S)
        body = m.group(1) if m else raw
        text = f"```yaml\n{body.strip()}\n```"
        try:
            check_background_text(text)
            return text
        except Exception as e:
            last = str(e)
            msgs += [{"role": "assistant", "content": raw[:6000]},
                     {"role": "user", "content": f"That BACKGROUND was rejected: {last}\nFix exactly these problems and output the complete YAML block again."}]
    raise CampaignError("the model could not write a valid BACKGROUND: " + last)
