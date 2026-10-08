from __future__ import annotations
import argparse
import sys

from .config import load_config


def main():
    ap = argparse.ArgumentParser(prog="gmhost", description="GM host for NEW ENGINE v5.0")
    sub = ap.add_subparsers(dest="cmd")
    s = sub.add_parser("serve", help="start the local web app (default)")
    s.add_argument("--port", type=int); s.add_argument("--no-browser", action="store_true")
    s.add_argument("--demo", action="store_true", help="use the built-in rule-based stand-in instead of a model")
    c = sub.add_parser("check", help="verify the installation (python, packages, engine files, model)")
    c.add_argument("--demo", action="store_true")
    c.add_argument("--load", action="store_true", help="also load the model and test schema-constrained output")
    p = sub.add_parser("play", help="play in the terminal")
    p.add_argument("campaign"); p.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    cfg = load_config()
    if getattr(a, "demo", False):
        cfg.model.backend = "mock"
    if a.cmd in (None, "serve"):
        from .server import serve
        serve(cfg, port=getattr(a, "port", None), open_browser=not getattr(a, "no_browser", False))
    elif a.cmd == "check":
        from .selfcheck import run
        sys.exit(run(cfg, load_model=a.load))
    elif a.cmd == "play":
        from .cli import play
        play(cfg, a.campaign)


if __name__ == "__main__":
    main()
