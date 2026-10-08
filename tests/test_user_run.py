# Copyright (c) 2026 West132.WL. All rights reserved.
"""Simulation of the user's real campaign (Ashfall: Hunter, saves R10..R120).

The saves are ground truth. Three simulations check the software against them:
1. REPLAY    – feed each save-to-save change set through the engine's own `merge` as a GM-Δ chain; the result must equal
               the next real save (the ledger pipeline reproduces the user's actual progression).
2. CONTINUE  – import every real save, play ten simulated rounds, and require a valid checkpoint save that carries every
               record of the imported one (the software can pick the campaign up at any point and keep it consistent).
3. CHAIN     – the whole R10..R120 series is valid and loses nothing.
"""
import copy
import re

import pytest

from gmhost import helper, saves
from gmhost.app import App
from gmhost.audit import audit, check_chain
from gmhost.demo import DemoBackend
from gmhost.campaign import normalize_background, write_background
from conftest import user_saves, ASHFALL_BG

SAVES = user_saves()
ROUNDS = sorted(SAVES)
_STAMP = re.compile(r"^R\d+:\s*")


def capsule(path):
    m = helper.mod()
    caps, retired = m._capsule_records(str(path))
    return {r["id"]: m._text_of(r) for r in caps}, {r["id"]: r["reason"] for r in retired}


def unstamp(t): return _STAMP.sub("", t or "")


def test_the_real_campaign_is_all_there():
    assert ROUNDS == [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]


def test_chain_is_valid_and_loses_nothing(tmp_path):
    lines = check_chain([SAVES[n] for n in ROUNDS], str(ASHFALL_BG))
    assert len(lines) == 12
    assert all("valid=True" in l for l in lines), "\n".join(lines)
    assert all("dropped=0" in l for l in lines if "vs R" in l)


@pytest.mark.parametrize("a,b", list(zip(ROUNDS, ROUNDS[1:])))
def test_replay_reproduces_the_next_real_save(a, b, tmp_path):
    """merge(save a + the changes that happened by b) == save b."""
    m = helper.mod()
    bgp = tmp_path / "bg.md"
    write_background(bgp, normalize_background(ASHFALL_BG.read_text(encoding="utf-8")))
    A, Aret = capsule(SAVES[a])
    B, Bret = capsule(SAVES[b])
    entries = []
    for rid, text in sorted(B.items()):
        old = A.get(rid)
        if old is not None and unstamp(old) == unstamp(text):
            continue
        if old is not None and text.startswith(old + " | "):         # a dated note appended to a whole record
            entries.append(("~", rid, text[len(old) + 3:]))
        else:
            entries.append(("+", rid, unstamp(text)))
    for rid, why in Bret.items():
        if rid not in Aret:
            entries.append(("-", rid, why or "retired"))
    blocks = [f"GM-Δ {n} none" for n in range(a + 1, b)]            # the quiet rounds in between, as the engine writes them
    stamp = "\n".join(blocks) + f"\nGM-Δ {b} ⟵ {b - 1}\n" + "\n".join(f"  {op} {rid} :: {c.replace(chr(10), ' ')}" for op, rid, c in entries) + "\n"
    chain = tmp_path / "chain.md"; chain.write_text(stamp, encoding="utf-8")
    out = m.do_merge(helper.ns(base=str(SAVES[a]), background=str(bgp), deltas=str(chain), out=None, save_round=b, encoding="plain"))
    cap = tmp_path / "cap.md"; cap.write_text(out["capsule_yaml"], encoding="utf-8")
    got, _ = capsule(cap)
    wrong = [rid for rid, t in B.items() if rid in got and unstamp(got[rid]) != unstamp(t)]
    bg = m._bg_tree(str(bgp))
    # `merge --background` leaves out records that merely repeat the BACKGROUND; everything else must be present
    missing = [rid for rid in B if rid not in got and not m._same_as_bg(bg, rid, B[rid])]
    assert not out.get("degraded") and not out.get("gaps")
    assert wrong == [] and missing == [], f"R{a}->R{b}: {len(wrong)} differ {wrong[:3]}, {len(missing)} missing {missing[:3]}"


@pytest.mark.parametrize("n", ROUNDS)
def test_continue_from_every_real_save(n, cfg, example_text, dice):
    """Import the real save, simulate ten rounds (waiting, a fight, a question, rest), save, validate against it."""
    dice(10, 7, 6, 8)
    app = App(cfg, DemoBackend())
    app.import_save(f"r{n}", SAVES[n].read_text(encoding="utf-8"), example_text)
    c = app.camp
    start = c.rnd
    assert start == n and c.player["condition"]["hp"] <= 16
    plan = ["I wait an hour", "I shoot the wolf", "I ask Nadia about her brother?", "I wait an hour", "I rest until morning"] + ["I wait an hour"] * 5
    last = None
    for text in plan:
        last = app.play(text)
        assert not last.get("blocked"), last
        assert last["round"] is not None
    assert c.rnd == start + 10
    assert last["save"] and last["save"]["valid"], last["save"]
    # the new save carries every record of the one we started from (the helper's own survival check)
    v = helper.mod().do_validate(helper.ns(file=last["save"]["path"], against=str(SAVES[n]), background=str(c.bg_path)))
    assert v["valid"], v["survival"]
    assert not [f for f in audit(c) if f.level == "error"]


def test_the_import_repairs_get_written_into_the_next_save(cfg, example_text, dice):
    dice(10)
    app = App(cfg, DemoBackend())
    app.import_save("rep", SAVES[120].read_text(encoding="utf-8"), example_text)
    for _ in range(10): r = app.play("I wait an hour")
    txt = open(r["save"]["path"], encoding="utf-8").read()
    assert "item_points: 1" in txt and "continuity_status.degraded.item_points_reserve" in txt
    assert "npcs.eli_voss.state.hp :: R121: 12" in txt
