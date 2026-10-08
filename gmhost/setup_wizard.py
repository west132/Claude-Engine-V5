# Copyright (c) 2026 West132.WL. All rights reserved.
"""First-run setup: check the computer, then for each missing item let the person choose to install it themselves
(we print the exact command) or let the program do it. Only steps that need no administrator rights are ever automated."""
from __future__ import annotations
import hashlib
import importlib
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path
from typing import Callable

from . import sysinfo

PIP_CMDS = {
    "pyyaml": ["pyyaml"],
    "llama_cpp": ["llama-cpp-python", "--extra-index-url", "https://abetlen.github.io/llama-cpp-python/whl/cpu"],
}


def pip_install(item: str, say: Callable[[str], None] = print) -> bool:
    """Install into the interpreter that is running this program (the private .venv when started by the launcher)."""
    if item not in PIP_CMDS:
        say(f"'{item}' cannot be installed automatically."); return False
    cmd = [sys.executable, "-m", "pip", "install", "--disable-pip-version-check", *PIP_CMDS[item]]
    say("Running: " + " ".join(cmd))
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in p.stdout:                                  # show progress as it happens
            line = line.rstrip()
            if line: say("  " + line[:200])
        ok = p.wait() == 0
    except Exception as e:
        say(f"Could not run pip: {e}"); return False
    importlib.invalidate_caches()
    if not ok:
        say("The install did not finish. " + ("There may be no ready-made package for this system and no C++ compiler. "
            "Alternative: install Ollama or LM Studio and point config.toml at it (see INSTALL.md)." if item == "llama_cpp" else "See the messages above."))
    return ok and sysinfo.have("llama_cpp" if item == "llama_cpp" else "yaml")


def download(url: str, dest_dir: Path, say: Callable[[str], None] = print, sha256: str | None = None) -> Path:
    """Fetch a direct .gguf link into models/ (resumes a partial file; prints the SHA-256 so you can compare it)."""
    if not url.lower().split("?")[0].endswith(".gguf"):
        raise ValueError("that link does not end in .gguf — paste the direct download link of the model file")
    dest_dir.mkdir(parents=True, exist_ok=True)
    name = url.split("?")[0].rsplit("/", 1)[1]
    dest = dest_dir / name
    part = dest.with_suffix(dest.suffix + ".part")
    have = part.stat().st_size if part.exists() else 0
    req = urllib.request.Request(url, headers={"Range": f"bytes={have}-"} if have else {})
    with urllib.request.urlopen(req, timeout=60) as r:
        resumed = have and r.status == 206
        total = int(r.headers.get("Content-Length") or 0) + (have if resumed else 0)
        done, last = (have if resumed else 0), -1
        with open(part, "ab" if resumed else "wb") as f:
            while True:
                chunk = r.read(1 << 20)
                if not chunk: break
                f.write(chunk); done += len(chunk)
                pct = int(100 * done / total) if total else -1
                if pct != last and (pct % 5 == 0 or pct < 0):
                    last = pct; say(f"  downloading {name}: {done / 2**30:.2f} GB" + (f" of {total / 2**30:.2f} GB ({pct}%)" if total else ""))
    part.replace(dest)
    h = hashlib.sha256()
    with open(dest, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""): h.update(b)
    digest = h.hexdigest()
    say(f"Saved {dest} — SHA-256 {digest}")
    if sha256 and digest.lower() != sha256.lower().replace("sha256:", ""):
        dest.unlink(); raise ValueError("the SHA-256 does not match the expected value; the file was deleted")
    return dest


def list_models(base_url: str, api_key: str = "") -> list[str]:
    """Ask an OpenAI-compatible server (Ollama, LM Studio, an API) which models it offers. Empty list = unreachable."""
    req = urllib.request.Request(base_url.rstrip("/") + "/models", headers={"Authorization": f"Bearer {api_key}"} if api_key else {})
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            return [m["id"] for m in json.loads(r.read().decode("utf-8")).get("data", []) if m.get("id")]
    except Exception:
        return []


def write_model_config(root: Path, **fields) -> Path:
    """Set the given keys in config.toml's [model] table, keeping every other setting (the old file is saved as config.toml.bak)."""
    path = root / "config.toml"
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    if text:
        (root / "config.toml.bak").write_text(text, encoding="utf-8")
    m = re.search(r"(?ms)^\[model\]\s*\n(.*?)(?=^\[|\Z)", text)
    body = m.group(1) if m else ""
    for k, v in fields.items():
        line = f"{k} = {json.dumps(v)}" if isinstance(v, str) else f"{k} = {v}"
        if re.search(rf"(?m)^{k}\s*=", body):
            body = re.sub(rf"(?m)^{k}\s*=.*$", lambda _: line, body)
        else:
            body = body.rstrip("\n") + ("\n" if body.strip() else "") + line + "\n"
    block = "[model]\n" + body.rstrip("\n") + "\n\n"
    text = (text[:m.start()] + block + text[m.end():]) if m else (text.rstrip("\n") + ("\n\n" if text.strip() else "") + block)
    path.write_text(text, encoding="utf-8")
    return path


MODES = """How do you want to run the AI?
  1) Test on this computer's CPU      the built-in engine, no extra program; slow, fine for trying it out
  2) Use an online API                OpenAI-compatible service with your own key (your story text is sent to that service)
  3) Set up a model for my graphics card   install LM Studio (free), which uses the GPU; best speed
  4) I already have a local AI        link Ollama, LM Studio or another local server"""

LMSTUDIO_STEPS = """LM Studio is a free app that downloads models and runs them on your graphics card. No command line, no compiler.
  a) Install it from https://lmstudio.ai (the normal installer works for one user).
  b) In LM Studio, search for an instruct model of the size recommended above and download its Q4_K_M version.
  c) Load the model. Set Context Length to 32768 and GPU Offload to the maximum.
  d) Open the Developer tab and press Start Server (it listens on http://127.0.0.1:1234)."""


def _pick_model(models: list[str], ask, say) -> str:
    if not models:
        return ""
    if len(models) == 1:
        say(f"  Found one model: {models[0]}"); return models[0]
    say("  Models found:" + "".join(f"\n    {i}) {m}" for i, m in enumerate(models, 1)))
    c = ask(f"  Choose 1-{len(models)} [1]: ").strip() or "1"
    return models[int(c) - 1] if c.isdigit() and 1 <= int(c) <= len(models) else models[0]


def connect(root: Path, mode: str, info: dict, ask, say) -> bool:
    """Modes 2-4: record where the AI lives in config.toml. Returns True when a server/model was linked."""
    if mode == "2":
        say("\nOnline API. The story text, character facts and your messages are sent to that provider; nothing is kept here but your key in config.toml.")
        url = ask("  API base URL [https://api.openai.com/v1]: ").strip() or "https://api.openai.com/v1"
        key = ask("  API key: ").strip()
        models = list_models(url, key)
        model = _pick_model(models, ask, say) or ask("  Model name: ").strip()
        if not models: say("  (could not list models; the settings are saved anyway, check the key and address if the app reports an error)")
    elif mode == "3":
        say("\n" + "\n".join(sysinfo.recommend(info)["lines"][:2]) + "\n")
        say(LMSTUDIO_STEPS)
        url, key = "http://127.0.0.1:1234/v1", ""
        while True:
            ask("\n  Press Enter when the server is running (or Ctrl+C to finish later): ")
            models = list_models(url)
            if models: break
            say("  I can't reach LM Studio's server yet. Is the model loaded and the server started?")
            if ask("  Try again? [Y/n]: ").strip().lower() == "n":
                say("  OK. Finish the steps, then run:  python -m gmhost setup"); return False
        model = _pick_model(models, ask, say)
    else:
        say("\nWhich local program?\n  1) Ollama (http://127.0.0.1:11434)\n  2) LM Studio (http://127.0.0.1:1234)\n  3) Another address")
        c = ask("  Choose 1-3 [1]: ").strip() or "1"
        url = {"1": "http://127.0.0.1:11434/v1", "2": "http://127.0.0.1:1234/v1"}.get(c) or ask("  Address ending in /v1: ").strip()
        key = "" if c in ("1", "2") else ask("  API key (Enter for none): ").strip()
        models = list_models(url, key)
        if not models:
            say("  I can't reach it. Start the program and load a model, then run:  python -m gmhost setup"); return False
        model = _pick_model(models, ask, say)
    write_model_config(root, backend="openai", base_url=url, model=model, api_key=key, n_ctx=32768)
    say(f"  Saved to config.toml: {model or '(model name empty)'} at {url}")
    if mode in ("3", "4"):
        say("  Reminder: the context length in that program must be 32768 or the AI will lose track of the story.")
    return True


def run(root: Path, auto: bool = False, check_only: bool = False, first_run: bool = False,
        ask: Callable[[str], str] = input, say: Callable[[str], None] = print) -> int:
    """Interactive wizard. Returns 0 when nothing essential is missing afterwards."""
    say("Checking your computer…\n")
    info = sysinfo.gather(root)
    say(sysinfo.format_report(info)); say("")
    local = True
    if not (auto or check_only):
        say(MODES)
        mode = ask("Choose 1-4 [1]: ").strip() or "1"
        if mode in ("2", "3", "4"):
            local = not connect(root, mode, info, ask, say)       # linked a server/API: no local engine or model file needed
        elif mode == "1":
            say("\nCPU test: use the smallest tier (a 3B-7B model). Expect minutes per turn; it is for trying the program, not for long play.")
        say("")
    todo = sysinfo.problems(info, local_model=local)
    if not todo:
        say("Everything the program needs is in place."); return 0
    say("Missing:" + "".join(f"\n  - {p['label']}" for p in todo))
    if check_only:
        return 1
    say("")
    for p in todo:
        say(f"\n{p['label']}")
        if not p["auto"]:
            say("  The program cannot do this one for you without changing your system, so:")
            say("  " + p["manual"])
            if p["id"] == "model":
                url = "" if auto else ask("  Paste a direct .gguf download link to let the program fetch it, or press Enter to do it yourself: ").strip()
                if url:
                    try: download(url, root / "models", say)
                    except Exception as e: say(f"  Download failed: {e}")
            continue
        choice = "1" if auto else ask("  1) Install it for me (no admin rights needed)   2) I will install it myself   3) Skip for now  [1]: ").strip() or "1"
        if choice == "2":
            say("  Run this in a terminal, then start the program again:\n  " + p["manual"])
        elif choice == "1":
            say("  Installing…" if pip_install(p["id"], say) else "  (not installed)")
        else:
            say("  Skipped.")
    say("\nRe-checking…")
    left = sysinfo.problems(sysinfo.gather(root))
    say("All set." if not left else "Still missing: " + ", ".join(x["id"] for x in left) + ". The program can still open; the Setup screen in the app shows how to finish.")
    return 0 if not left else 1
