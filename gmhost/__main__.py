# Copyright (c) 2026 West132.WL. All rights reserved.
from __future__ import annotations
import argparse
import sys

from .config import load_config


def main():
    ap = argparse.ArgumentParser(prog="gmhost", description="GM host for NEW ENGINE v5.0")
    sub = ap.add_subparsers(dest="cmd")
    s = sub.add_parser("serve", help="start the local web app (default)")
    s.add_argument("--port", type=int); s.add_argument("--no-browser", action="store_true")
    s.add_argument("--tailscale", action="store_true", help="also listen on this machine's Tailscale address")
    s.add_argument("--host", help="address to listen on (default 127.0.0.1)")
    s.add_argument("--demo", action="store_true", help="use the built-in rule-based stand-in instead of a model")
    c = sub.add_parser("check", help="verify the installation (python, packages, engine files, model)")
    c.add_argument("--demo", action="store_true")
    c.add_argument("--load", action="store_true", help="also load the model and test schema-constrained output")
    au = sub.add_parser("audit", help="audit a save against its BACKGROUND (engine rules beyond validate)")
    au.add_argument("save"); au.add_argument("background")
    su = sub.add_parser("setup", help="check this computer and install what is missing (asks first)")
    su.add_argument("--check", action="store_true", help="only report; change nothing")
    su.add_argument("--auto", action="store_true", help="install everything that needs no admin rights, without asking")
    su.add_argument("--first-run", action="store_true")
    pt = sub.add_parser("playtest", help="play a short easy scripted session on a simple world and write playtest_report.md")
    pt.add_argument("--background", default="examples/harbour_guesthouse/background.md"); pt.add_argument("--language", default="en")
    ch = sub.add_parser("chain", help="check a series of saves, oldest to newest, for gaps and silent losses")
    ch.add_argument("background"); ch.add_argument("saves", nargs="+")
    p = sub.add_parser("play", help="play in the terminal")
    p.add_argument("campaign"); p.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    cfg = load_config()
    if getattr(a, "demo", False):
        cfg.model.backend = "mock"
    if a.cmd in (None, "serve"):
        from .server import serve
        serve(cfg, port=getattr(a, "port", None), open_browser=not getattr(a, "no_browser", False),
              tailscale=True if getattr(a, "tailscale", False) else None, host=getattr(a, "host", None))
    elif a.cmd == "check":
        from .selfcheck import run
        sys.exit(run(cfg, load_model=a.load))
    elif a.cmd == "audit":
        import shutil, tempfile
        from pathlib import Path
        from . import helper, saves
        from .audit import audit, report
        from .config import Config
        helper.load(cfg.engine_dir)
        tmp = Path(tempfile.mkdtemp()); shutil.copytree(cfg.engine_dir, tmp / "engine"); (tmp / "campaigns").mkdir()
        c = saves.import_save(Config(root=tmp), "audit", Path(a.save).read_text(encoding="utf-8"), Path(a.background).read_text(encoding="utf-8"))
        print("repairs the importer would make:\n  " + "\n  ".join(c.session.get("import_repairs") or ["none"]))
        print(report(audit(c)))
        shutil.rmtree(tmp, ignore_errors=True)
    elif a.cmd == "setup":
        from .setup_wizard import run as setup_run
        sys.exit(setup_run(cfg.root, auto=a.auto, check_only=a.check, first_run=a.first_run))
    elif a.cmd == "playtest":
        from pathlib import Path
        from .playtest import run as playtest_run
        playtest_run(cfg, Path(a.background), a.language)
    elif a.cmd == "chain":
        from . import helper
        from .audit import check_chain
        helper.load(cfg.engine_dir)
        print("\n".join(check_chain(a.saves, a.background)))
    elif a.cmd == "play":
        from .cli import play
        play(cfg, a.campaign)


if __name__ == "__main__":
    main()
