"""`python -m gmhost check` — verifies an installation without needing a model."""
from __future__ import annotations
import shutil
import sys
import tempfile
from pathlib import Path

from .config import Config


def run(cfg: Config, load_model: bool = False) -> int:
    ok = True
    def line(good, msg):
        nonlocal ok
        ok = ok and good
        print(("  ok   " if good else "  FAIL ") + msg)
    print("GM host installation check")
    line(sys.version_info >= (3, 11), f"Python {sys.version.split()[0]} (needs 3.11+)")
    try:
        import yaml; line(True, f"PyYAML {yaml.__version__}")
    except ImportError:
        line(False, "PyYAML missing: pip install pyyaml")
        return 1
    try:
        from . import helper
        from .cards import Engine
        helper.load(cfg.engine_dir)
        eng = Engine(cfg.engine_dir)
        line(True, f"engine v{eng.version}: {len(eng.routes)} routing rows, {len(eng.sec)} sections, helper v{helper.mod().ENGINE_VERSION}")
        for f in ("AI_RULES", "BACKGROUND_TEMPLATE", "SAVE_TEMPLATE"):
            line(bool(list(cfg.engine_dir.glob(f"{f}_v*.md"))), f"{f} present")
    except Exception as e:
        line(False, f"engine files: {e}")
        return 1
    ggufs = list(cfg.models_dir.glob("**/*.gguf"))
    try:
        import llama_cpp; have_llama = llama_cpp.__version__
    except Exception:
        have_llama = None
    print(f"  info models/: {[g.name for g in ggufs] or 'no .gguf file yet'}; llama-cpp-python: {have_llama or 'not installed'}; "
          f"backend setting: {cfg.model.backend}")
    if cfg.model.backend in ("auto", "llama_cpp") and ggufs and not have_llama:
        line(False, "a .gguf is present but llama-cpp-python is not installed (see INSTALL.md)")
    # offline end-to-end self-test with the stand-in model: 10 rounds -> checkpoint save -> reload
    from .app import App
    from .demo import DemoBackend
    from .campaign import Campaign
    from . import saves
    tmp = Path(tempfile.mkdtemp())
    try:
        shutil.copytree(cfg.engine_dir, tmp / "engine")
        shutil.copytree(cfg.root / "examples", tmp / "examples")
        c2 = Config(root=tmp); c2.model.backend = "mock"
        app = App(c2, DemoBackend())
        ex = app.examples()[0]
        app.create("selftest", ex["text"])
        app.opening()
        last = None
        for _ in range(10):
            last = app.play("I wait an hour")
        s = last["save"]
        line(bool(s and s.get("valid")), f"10-round self-test: checkpoint save valid ({Path(s['path']).name if s else 'none'})")
        txt = Path(s["path"]).read_text(encoding="utf-8")
        saves.import_save(c2, "selftest2", txt, (tmp / "campaigns/selftest/background.md").read_text(encoding="utf-8"))
        line(True, "save re-imports and validates")
    except Exception as e:
        line(False, f"self-test: {type(e).__name__}: {e}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    if load_model:
        try:
            from .llm import make_backend
            b = make_backend(cfg)
            out = b.chat([{"role": "user", "content": 'Reply with the JSON {"ok": true}'}], max_tokens=30, temperature=0.0,
                         schema={"type": "object", "properties": {"ok": {"type": "boolean"}}, "required": ["ok"]})
            line('true' in out.lower(), f"model loaded ({b.name}, n_ctx {b.n_ctx}) and produced schema-constrained JSON: {out.strip()[:60]}")
        except Exception as e:
            line(False, f"model: {e}")
    print("\nAll good." if ok else "\nSome checks failed — see INSTALL.md.")
    return 0 if ok else 1
