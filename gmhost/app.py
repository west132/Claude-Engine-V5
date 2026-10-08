# Copyright (c) 2026 West132.WL. All rights reserved.
"""Application service: campaigns, the model, and the Game, behind one lock (single local user)."""
from __future__ import annotations
import json
import shutil
import threading
from pathlib import Path

from . import bgen, helper, i18n, saves
from .campaign import Campaign, CampaignError
from .config import Config, load_config
from .llm import Backend, LLMError, make_backend
from .turn import Game, TurnError, status_panel, TurnResult


class App:
    def __init__(self, cfg: Config | None = None, backend: Backend | None = None):
        self.cfg = cfg or load_config()
        helper.load(self.cfg.engine_dir)
        self.cfg.campaigns_dir.mkdir(exist_ok=True)
        self.lock = threading.RLock()
        self.backend, self.game, self.model_error = None, None, None
        self.camp: Campaign | None = None
        if backend is not None:
            self._attach(backend)
        else:
            self.load_model()

    def _attach(self, backend):
        self.backend = backend
        try:
            self.game = Game(self.cfg, backend)
            self.model_error = None
        except TurnError as e:
            self.game, self.model_error = None, str(e)

    def load_model(self):
        try:
            self._attach(make_backend(self.cfg))
        except (LLMError, Exception) as e:               # the UI shows install help instead of crashing
            self.backend, self.game, self.model_error = None, None, str(e)

    # ---- preferences (remembered across restarts and devices) ------------------------------------
    @property
    def _prefs_path(self) -> Path:
        return self.cfg.root / "prefs.json"

    def prefs(self) -> dict:
        try:
            d = json.loads(self._prefs_path.read_text(encoding="utf-8"))
        except Exception:
            d = {}
        lang = d.get("language")
        return {"language": i18n.normalize(lang or self.cfg.game.language), "language_set": lang in i18n.LANGUAGES}

    def set_language(self, lang: str) -> dict:
        if lang not in i18n.LANGUAGES:
            raise CampaignError(f"language must be one of {list(i18n.LANGUAGES)}")
        self._prefs_path.write_text(json.dumps({"language": lang}), encoding="utf-8")
        return self.prefs()

    # ---- info -------------------------------------------------------------------------------
    def info(self) -> dict:
        return {"model": {"ready": self.game is not None, "name": getattr(self.backend, "name", None),
                          "path": str(getattr(self.backend, "path", "") or ""), "n_ctx": getattr(self.backend, "n_ctx", None),
                          "error": self.model_error},
                "engine": self.game.engine.version if self.game else None,
                "campaigns": self.list_campaigns(), "current": self.camp.name if self.camp else None,
                "prefs": self.prefs(), "languages": i18n.LANGUAGES,
                "defaults": {"language": self.prefs()["language"], "profile": self.cfg.game.profile, "encoding": self.cfg.game.encoding}}

    def list_campaigns(self) -> list[dict]:
        out = []
        for d in sorted(self.cfg.campaigns_dir.iterdir()) if self.cfg.campaigns_dir.exists() else []:
            if (d / "work" / "journal.json").exists():
                try:
                    j = json.loads((d / "work" / "journal.json").read_text(encoding="utf-8"))
                    rd = j["readable"]
                    out.append({"name": d.name, "round": rd["round"]["last_completed_round"],
                                "saved": rd["round"]["saved_completed_round"],
                                "character": rd["player"].get("identity", {}).get("name"), "language": rd.get("language")})
                except Exception:
                    out.append({"name": d.name, "round": "?", "saved": "?", "character": "?"})
        return out

    def examples(self) -> list[dict]:
        out = []
        for p in sorted((self.cfg.root / "examples").glob("*/background.md")):
            out.append({"id": p.parent.name, "text": p.read_text(encoding="utf-8")})
        return out

    # ---- campaigns ---------------------------------------------------------------------------
    def create(self, name, background_text=None, premise=None, language=None, profile=None, encoding=None,
               on_event=lambda e: None, fill=None) -> dict:
        with self.lock:
            if background_text is None:
                if not premise: raise CampaignError("give a BACKGROUND file or a premise")
                if self.backend is None: raise CampaignError("a premise needs a model; none is loaded")
                tmpl = (self.cfg.engine_dir / sorted(p.name for p in self.cfg.engine_dir.glob("BACKGROUND_TEMPLATE_v*.md"))[-1]).read_text(encoding="utf-8")
                background_text = bgen.generate(self.backend, tmpl, premise, language or self.cfg.game.language, True, on_event)
            else:
                bgen.check_background_text(background_text)
            language = i18n.normalize(language or self.prefs()["language"])
            self.camp = Campaign.create(self.cfg, name, background_text, language, profile, encoding, fill)
            self.set_language(language)
            return {"name": name}

    def unassigned(self, background_text: str) -> list[dict]:
        from .campaign import normalize_background
        return bgen.unassigned(normalize_background(background_text))

    def open(self, name) -> Campaign:
        with self.lock:
            self.camp = Campaign.open(self.cfg, name)
            return self.camp

    def import_save(self, name, save_text, background_text):
        with self.lock:
            self.camp = saves.import_save(self.cfg, name, save_text, background_text)

    def need(self) -> Campaign:
        if self.camp is None: raise CampaignError("open or create a campaign first")
        return self.camp

    def need_game(self) -> Game:
        if self.game is None: raise TurnError(self.model_error or "no model loaded")
        return self.game

    # ---- play -------------------------------------------------------------------------------
    def snapshot(self) -> dict:
        c = self.need()
        return {"status": status_panel(c), "history": c.session["history"][-60:],
                "needs_opening": c.rnd == 0 and not c.session["history"], "dues": c.session.get("dues"),
                "saves": sorted(p.name for p in c.saves.glob("save_*.md"))}

    def opening(self, on_event=lambda e: None) -> dict:
        with self.lock:
            r = self.need_game().opening(self.need(), on_event)
            return r.to_dict()

    def play(self, text, on_event=lambda e: None) -> dict:
        with self.lock:
            r = self.need_game().play(self.need(), text, on_event)
            return r.to_dict()

    def save(self, on_event=lambda e: None) -> dict:
        with self.lock:
            return self.need_game().save(self.need(), on_event)

    def continue_unsaved(self):
        with self.lock:
            self.need_game().continue_unsaved(self.need())

    def set_options(self, profile=None, language=None, encoding=None):
        with self.lock:
            c = self.need()
            if encoding is not None:                          # engine §8.1: on the player's request, from now on
                if encoding not in ("plain", "b64", "rot13"): raise CampaignError("encoding must be plain, b64 or rot13")
                c.session["encoding"] = encoding
            if profile in ("full", "lite"): c.readable["profile"] = profile; c.closed_readable["profile"] = profile
            if language:
                language = i18n.normalize(language)
                c.readable["language"] = language; c.closed_readable["language"] = language
                self.set_language(language)                       # the last selected language is the one remembered
            c.write_journal()

    def prompts_file(self) -> Path:
        p = self.need().work / "last_turn_prompts.md"
        if not p.exists(): raise CampaignError("nothing sent to the AI yet: play a turn first")
        return p

    def gm_log(self, spoilers: bool) -> str:
        c = self.need()
        out = []
        for b in c.blocks:
            out.append(f"GM-Δ {b.round} ⟵ {b.prev}" if b.entries else f"GM-Δ {b.round} none")
            for e in b.entries:
                out.append(f"  {e.op} {e.id} :: " + (e.content if (spoilers or not e.hidden) else "[hidden]"))
        return "\n".join(out) or "(no GM-Δ since the last save)"

    def save_file(self, filename: str) -> Path:
        c = self.need()
        p = (c.saves / filename).resolve()
        if p.parent != c.saves.resolve() or not p.exists():
            raise CampaignError("no such save")
        return p

    def background_file(self) -> Path:
        return self.need().bg_path
