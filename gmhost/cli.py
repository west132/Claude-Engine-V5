# Copyright (c) 2026 West132.WL. All rights reserved.
"""Terminal front end (same engine, no browser)."""
from __future__ import annotations
from .app import App
from .campaign import CampaignError


def _show(r: dict):
    if r.get("header"): print("\n" + r["header"])
    for l in r.get("lines", []): print("  " + l.replace("\n", "\n  "))
    for s in r.get("status", []): print("  · " + s)
    print("\n" + (r.get("narration") or ""))
    if r.get("decision"):
        print("\n" + r["decision"]["question"])
        for i, o in enumerate(r["decision"]["options"], 1): print(f"  {i}. {o}")
    sv = r.get("save")
    if sv: print("\n[save] " + (f"FAILED: {sv['failed']}" if sv.get("failed") else f"R{sv['round']} → {sv['path']}"))
    for w in r.get("warnings", []): print("[note] " + w)
    if r.get("ended"): print("\n*** your character is dead ***")


def play(cfg, name: str):
    app = App(cfg)
    if app.model_error:
        print(app.model_error); return
    try:
        app.open(name)
    except CampaignError as e:
        print(e); return
    if app.camp.rnd == 0 and not app.camp.session["history"]:
        _show(app.opening(lambda e: None))
    print("(/save  /status  /quit)")
    while True:
        try:
            t = input("\n› ").strip()
        except EOFError:
            break
        if t in ("/quit", "/q"): break
        if t == "/save": print(app.save()); continue
        if t == "/status": print(app.snapshot()["status"]); continue
        if t:
            try: _show(app.play(t, lambda e: print("  …", e.get("text") or e.get("tool"), end="\r")))
            except Exception as e: print("error:", e)
