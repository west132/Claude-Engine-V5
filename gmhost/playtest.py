# Copyright (c) 2026 West132.WL. All rights reserved.
"""A short, easy, repeatable play session against the real model, with a written report. Use it to see how a model really behaves on a
simple world: `python -m gmhost playtest`. The report is written after every turn, so a slow model still leaves something to read."""
from __future__ import annotations
import re
import time
from pathlib import Path

from . import helper, llm
from .campaign import Campaign
from .config import Config
from .turn import Game

EASY = {
    "en": ["What should I do?", "I ask Hobb Marren for a room for the night.", "I ask him where I can find Tobias Wren.",
           "I walk to Mill Lane and go up to the Net Loft.", "I hand Tobias the envelope and ask him to sign for it.", "Recap: what has happened so far?"],
    "zh_hans": ["我现在要做什么？", "我向霍布·马伦要一间房过夜。", "我问他在哪里能找到托拜厄斯·雷恩。",
                "我走到磨坊巷，上到织网阁楼。", "我把信封交给托拜厄斯，请他签收。", "回顾一下到目前为止发生了什么？"],
}
_CJK = re.compile(r"[一-鿿]")


def run(cfg: Config, background: Path, language: str = "en", turns: list[str] | None = None, report: Path | None = None,
        say=print) -> Path:
    helper.load(cfg.engine_dir)
    backend = llm.make_backend(cfg)
    game = Game(cfg, backend)
    name = f"playtest_{int(time.time())}"
    camp = Campaign.create(cfg, name, background.read_text(encoding="utf-8"), language)
    report = report or (cfg.root / "playtest_report.md")
    out = [f"# Playtest report — {backend.name} {getattr(backend, 'model', '') or getattr(backend, 'path', '')}",
           f"World: {background.parent.name} · language: {language} · campaign folder: campaigns/{name}\n"]
    def flush(): report.write_text("\n".join(out), encoding="utf-8")
    start = time.time()
    say("opening…")
    res = game.opening(camp)
    out += ["## Opening", f"_{time.time() - start:.0f}s_\n", res.narration, ""]; flush()
    for text in (turns or EASY.get(language, EASY["en"])):
        t0 = time.time()
        say(f"> {text}")
        try:
            r = game.play(camp, text)
            body = [f"**Round:** {r.round}" if r.round else "**No round** (a question or a menu)"]
            if r.header: body.append(f"`{r.header}`")
            if r.lines: body.append("```\n" + "\n".join(r.lines) + "\n```")
            if r.status: body.append("Changes: " + "; ".join(r.status))
            body.append(r.narration)
            if r.decision: body.append("Options: " + " | ".join(r.decision["options"]))
            if r.warnings: body.append("Warnings: " + " | ".join(r.warnings))
            notes = []
            if language == "zh_hans" and not _CJK.search(r.narration): notes.append("narration is not in Chinese")
            if r.narration.count("\n") == 0 and len(r.narration) < 25: notes.append("very short narration")
            if notes: body.append("Auto-notes: " + "; ".join(notes))
            out += [f"## > {text}", f"_{time.time() - t0:.0f}s_\n", *body, ""]
        except Exception as e:
            out += [f"## > {text}", f"_{time.time() - t0:.0f}s_\n", f"**ERROR:** {type(e).__name__}: {e}", ""]
        flush()
    p = camp.player
    out += ["## End state", f"Location: {camp.location_name()} · time: {camp.time} · money: {p.get('money')} · round: {camp.rnd}",
            f"Quest: {(camp.tree().get('quests') or {}).get('deliver_the_envelope')}" if "deliver_the_envelope" in str(camp.tree().get("quests")) else ""]
    flush()
    say(f"report: {report}")
    return report
