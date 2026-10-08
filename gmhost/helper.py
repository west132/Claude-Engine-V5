"""Loads the engine's own stateless helper (engine/engine_math_v5_0.py) unmodified.

The helper is the single authority for dice, check maths, XP, harm, merge and
validate. This module only imports it and gives callers keyword-style access.
"""
from __future__ import annotations
import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace

_mod = None


def load(engine_dir: Path):
    global _mod
    if _mod is not None:
        return _mod
    files = sorted(engine_dir.glob("engine_math_v*.py"))
    if not files:
        raise FileNotFoundError(f"no engine_math_v*.py in {engine_dir}")
    spec = importlib.util.spec_from_file_location("engine_math", files[-1])
    m = importlib.util.module_from_spec(spec)
    sys.modules["engine_math"] = m
    spec.loader.exec_module(m)
    _mod = m
    return m


def mod():
    if _mod is None:
        raise RuntimeError("helper not loaded")
    return _mod


InputError = lambda: mod().InputError   # noqa: E731  (resolved lazily)


def ns(**kw):
    return SimpleNamespace(**kw)


def check_ns(**kw):
    """Namespace with every field do_check reads, defaulted."""
    d = dict(cmp=None, challenge=None, capmod=None, base=None, fit=0, condition=0,
             environment=0, time=0, sensory=0, position=0, simultaneous=0,
             brief=False, lite=False, basis=None, stakes=None, tool_source=None,
             label=None, odds=False, on_failure=None)
    d.update(kw)
    return SimpleNamespace(**d)
