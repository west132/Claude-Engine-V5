#!/usr/bin/env bash
# Copyright (c) 2026 West132.WL. All rights reserved.
# Launcher (Linux / macOS). Asks before installing anything; nothing outside this folder is changed.
set -e
cd "$(dirname "$0")"
PY=${PYTHON:-python3}
if ! "$PY" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)' 2>/dev/null; then
  echo "This program needs Python 3.11 or newer and it was not found."
  echo "Install it from python.org (choose 'Install for me only' - no admin needed), then run this again."
  exit 1
fi
if [ ! -d .venv ]; then
  echo "First run. The program needs a small Python package (PyYAML); the setup then asks how you want to run the AI."
  echo "They go into a private folder (.venv) inside this directory: no administrator rights, nothing changes in your system."
  echo "  1) Let the program set it up for me (needs internet once)"
  echo "  2) I will do it myself (show me the commands)"
  read -r -p "Choose 1 or 2 [1]: " choice; choice=${choice:-1}
  if [ "$choice" = "2" ]; then
    echo; echo "Run these, then start this launcher again:"
    echo "  $PY -m venv .venv"
    echo "  . .venv/bin/activate"
    echo "  pip install pyyaml"
    echo "  python -m gmhost setup      # checks your computer, installs the rest only if you say yes"
    exit 0
  fi
  "$PY" -m venv .venv
  . .venv/bin/activate
  pip install --disable-pip-version-check pyyaml
  python -m gmhost setup --first-run || true      # checks the computer; asks before anything else is installed
else
  . .venv/bin/activate
fi
python -m gmhost "$@"
