import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from gmhost import helper                       # noqa: E402
from gmhost.config import Config                # noqa: E402


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
    return (ROOT / "examples/the_salt_road/background.md").read_text(encoding="utf-8")


@pytest.fixture
def camp(cfg, example_text):
    from gmhost.campaign import Campaign
    return Campaign.create(cfg, "t", example_text)
