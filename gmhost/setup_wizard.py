# Copyright (c) 2026 West132.WL. All rights reserved.
"""First-run setup: check the computer, then for each missing item let the person choose to install it themselves
(we print the exact command) or let the program do it. Only steps that need no administrator rights are ever automated."""
from __future__ import annotations
import hashlib
import importlib
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


def run(root: Path, auto: bool = False, check_only: bool = False, first_run: bool = False,
        ask: Callable[[str], str] = input, say: Callable[[str], None] = print) -> int:
    """Interactive wizard. Returns 0 when nothing essential is missing afterwards."""
    say("Checking your computer…\n")
    info = sysinfo.gather(root)
    say(sysinfo.format_report(info)); say("")
    todo = sysinfo.problems(info)
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
