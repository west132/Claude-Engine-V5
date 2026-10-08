# Copyright (c) 2026 West132.WL. All rights reserved.
import re
import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from gmhost import helper                       # noqa: E402
from gmhost.config import Config                # noqa: E402

DATA = ROOT / "tests" / "data" / "ashfall"
ASHFALL_BG = ROOT / "examples" / "ashfall_hunter" / "background.md"


def user_saves() -> dict[int, Path]:
    """The user's real campaign: saves R10..R120 of Ashfall: Hunter."""
    return {int(re.search(r"_R(\d+)", p.name).group(1)): p for p in DATA.glob("save_ashfall_hunter_R*.md")}


class FakeRNG:
    """Deterministic dice: returns the queued values (clamped to the die) in order, cycling."""
    def __init__(self, vals): self.vals, self.i = list(vals), 0
    def randint(self, a, b):
        v = self.vals[self.i % len(self.vals)]; self.i += 1
        return max(a, min(b, v))


@pytest.fixture
def cfg(tmp_path):
    shutil.copytree(ROOT / "engine", tmp_path / "engine")
    shutil.copytree(ROOT / "examples", tmp_path / "examples")
    (tmp_path / "campaigns").mkdir()
    c = Config(root=tmp_path)
    c.model.backend = "mock"
    helper.load(c.engine_dir)
    return c


@pytest.fixture
def dice(monkeypatch):
    real = helper.mod()._rng
    def setter(*vals):
        monkeypatch.setattr(helper.mod(), "_rng", FakeRNG(vals))
    yield setter
    helper.mod()._rng = real


@pytest.fixture
def example_text():
    """Ashfall: Hunter BACKGROUND (the user's world)."""
    return ASHFALL_BG.read_text(encoding="utf-8")


@pytest.fixture
def camp(cfg, example_text):
    """A new Ashfall campaign at Round 0."""
    from gmhost.campaign import Campaign
    return Campaign.create(cfg, "t", example_text)


@pytest.fixture
def r120(cfg, example_text):
    """The user's real campaign state at R120 (day 26, 2026-11-01 21:40)."""
    from gmhost import saves
    return saves.import_save(cfg, "r120", user_saves()[120].read_text(encoding="utf-8"), example_text)


@pytest.fixture(autouse=True)
def _helper_loaded():
    helper.load(ROOT / "engine")
