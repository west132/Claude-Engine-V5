#!/usr/bin/env bash
# One-click launcher (Linux / macOS). First run creates a private Python environment and installs what is needed.
set -e
cd "$(dirname "$0")"
PY=${PYTHON:-python3}
if [ ! -d .venv ]; then
  echo "First run: creating environment (needs internet once)…"
  "$PY" -m venv .venv
  . .venv/bin/activate
  pip install --upgrade pip >/dev/null
  pip install pyyaml
  # llama.cpp runtime for .gguf models; falls back to a source build if no prebuilt wheel fits
  pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu || \
    echo "!! llama-cpp-python could not be installed. You can still use Ollama / LM Studio (see INSTALL.md)."
else
  . .venv/bin/activate
fi
python -m gmhost "$@"
