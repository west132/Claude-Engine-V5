"""The four shipped worlds and a real R120 chat save must load, audit and repair cleanly."""
from pathlib import Path

import pytest

from gmhost import bgen, saves
from gmhost.audit import audit
from gmhost.campaign import Campaign, CampaignError, normalize_background

ROOT = Path(__file__).resolve().parents[1]
WORLDS = ["tarnstead_low_fantasy", "ashfall_hunter", "cyberpunk_red_south_nc", "last_scion_boundary"]


def text(w): return (ROOT / "examples" / w / "background.md").read_text(encoding="utf-8")


@pytest.mark.parametrize("w", WORLDS)
def test_world_validates_and_starts(cfg, w):
    import shutil
    shutil.copytree(ROOT / "examples" / w, cfg.root / "examples" / w, dirs_exist_ok=True)
    tree = normalize_background(text(w))
    assert bgen.problems(tree) == []
    fill = {f["path"]: "Test" for f in bgen.unassigned(tree)}
    c = Campaign.create(cfg, "w", text(w), fill=fill)
    assert not [f for f in audit(c) if f.level == "error"]
    assert "[UNASSIGNED" not in str(c.player)


def test_unassigned_must_be_filled_before_round_one(cfg):
    assert bgen.unassigned(normalize_background(text("tarnstead_low_fantasy")))
    with pytest.raises(CampaignError, match="still unassigned"):
        Campaign.create(cfg, "t", text("tarnstead_low_fantasy"))
    c = Campaign.create(cfg, "t2", text("tarnstead_low_fantasy"),
                        fill={f["path"]: "X" for f in bgen.unassigned(normalize_background(text("tarnstead_low_fantasy")))})
    assert c.player["identity"]["name"] == "X"


def test_r120_save_imports_validates_and_is_repaired(cfg):
    save = (ROOT / "tests/data/save_ashfall_hunter_R120.md").read_text(encoding="utf-8")
    c = saves.import_save(cfg, "ash", save, text("ashfall_hunter"))
    assert c.rnd == 120 and c.player["item_points"] == 1 and "starting_item_points" not in c.player
    notes = " ".join(c.session["import_repairs"])
    assert "item_points" in notes and "glass_spread.clock.filled" in notes and "npcs.eli_voss.state.hp" in notes
    assert "unknown" in notes
    # repairs are real GM-Δ entries that merge and then validate as the next save
    c.commit_block(c.make_block(121, []))
    assert c.get("active_world_pressures.glass_spread.clock.filled") == 4
    assert c.get("npcs.eli_voss.state.hp") == 12
    assert c.get("active_world_pressures.glass_spread.clock.due") == "2026-11-03"
    assert c.get("npcs.dutch_haller.job") == "unknown"
    assert c.get("npcs.dutch_haller.name") == "Dutch Haller"          # taken from the save's own index line
    c.readable["round"]["last_completed_round"] = 121
    c.closed_readable = __import__("copy").deepcopy(c.readable)
    assert saves.build_save(c)["valid"]
    assert [f for f in audit(c) if f.level == "error"] == []


def test_mp_is_recognised_from_ability_text(cfg):
    save = (ROOT / "tests/data/save_ashfall_hunter_R120.md").read_text(encoding="utf-8")
    c = saves.import_save(cfg, "ash2", save, text("ashfall_hunter"))
    assert not [f for f in audit(c) if "MP-drawing" in f.msg]
