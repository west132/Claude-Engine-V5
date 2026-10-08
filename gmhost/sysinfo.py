# Copyright (c) 2026 West132.WL. All rights reserved.
"""Look at this computer (standard library only, so it works before anything is installed) and recommend a model size."""
from __future__ import annotations
import importlib.util
import json
import os
import platform
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

MIN_PYTHON = (3, 11)
# Model tiers: parameters (billions) -> KV-cache GB at a 32k context (typical grouped-query models, f16 cache)
TIERS = [(3, 1.2), (7, 1.9), (14, 6.4), (32, 8.6), (70, 10.7)]
GB_PER_B = 0.65          # Q4_K_M file size per billion parameters (approx.)
OVERHEAD_GB = 1.0


def _run(cmd, timeout=6):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout).stdout.strip()
    except Exception:
        return ""


def _ram_gb() -> tuple[float, float]:
    """(total, available) in GB; (0, 0) if unknown."""
    s = platform.system()
    try:
        if s == "Linux":
            kv = {l.split(":")[0]: int(l.split()[1]) for l in open("/proc/meminfo") if ":" in l}
            return kv["MemTotal"] / 1048576, kv.get("MemAvailable", kv["MemFree"]) / 1048576
        if s == "Darwin":
            total = int(_run(["sysctl", "-n", "hw.memsize"])) / 2**30
            vm = _run(["vm_stat"]); page = 4096
            free = 0
            for line in vm.splitlines():
                if line.startswith("page size"): page = int(line.split()[-2])
                if line.split(":")[0] in ("Pages free", "Pages inactive", "Pages speculative"):
                    free += int(line.split(":")[1].strip(" .")) * page
            return total, free / 2**30
        if s == "Windows":
            import ctypes
            class MS(ctypes.Structure):
                _fields_ = [("l", ctypes.c_ulong), ("load", ctypes.c_ulong), ("tp", ctypes.c_ulonglong), ("ap", ctypes.c_ulonglong),
                            ("tv", ctypes.c_ulonglong), ("av", ctypes.c_ulonglong), ("te", ctypes.c_ulonglong), ("ae", ctypes.c_ulonglong), ("x", ctypes.c_ulonglong)]
            m = MS(); m.l = ctypes.sizeof(MS); ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
            return m.tp / 2**30, m.ap / 2**30
    except Exception:
        pass
    return 0.0, 0.0


def _gpu() -> dict:
    out = _run(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader,nounits"])
    if out:
        try:
            name, mem = [x.strip() for x in out.splitlines()[0].split(",")]
            return {"kind": "nvidia", "name": name, "vram_gb": round(int(mem) / 1024, 1)}
        except Exception:
            pass
    if platform.system() == "Darwin" and platform.machine() == "arm64":
        return {"kind": "apple", "name": "Apple Silicon (unified memory)", "vram_gb": 0}
    return {"kind": "none", "name": "no supported GPU found", "vram_gb": 0}


def _server(url) -> bool:
    try:
        urllib.request.urlopen(url, timeout=1.0).read(64)
        return True
    except Exception:
        return False


def have(module: str) -> bool:
    return importlib.util.find_spec(module) is not None


def gather(root: Path) -> dict:
    total, avail = _ram_gb()
    disk = shutil.disk_usage(root if root.exists() else root.parent)
    models = sorted((root / "models").glob("**/*.gguf")) if (root / "models").exists() else []
    return {
        "os": f"{platform.system()} {platform.release()} ({platform.machine()})",
        "cpu_cores": os.cpu_count() or 0,
        "ram_gb": round(total, 1), "ram_free_gb": round(avail, 1),
        "disk_free_gb": round(disk.free / 2**30, 1),
        "gpu": _gpu(),
        "python": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "python_ok": sys.version_info >= MIN_PYTHON,
        "in_venv": sys.prefix != getattr(sys, "base_prefix", sys.prefix),
        "pyyaml": have("yaml"),
        "llama_cpp": have("llama_cpp"),
        "compiler": next((c for c in ("gcc", "clang", "cl") if shutil.which(c)), None),
        "cmake": bool(shutil.which("cmake")),
        "models": [{"name": m.name, "gb": round(m.stat().st_size / 2**30, 2)} for m in models],
        "ollama": _server("http://127.0.0.1:11434/api/tags"),
        "lmstudio": _server("http://127.0.0.1:1234/v1/models"),
    }


def need_gb(b: int) -> float:
    kv = dict(TIERS)[b]
    return round(GB_PER_B * b + kv + OVERHEAD_GB, 1)


def budget(info: dict) -> tuple[float, str]:
    g, ram = info["gpu"], info["ram_gb"]
    if g["kind"] == "nvidia" and g["vram_gb"]:
        return round(g["vram_gb"] * 0.95, 1), f"GPU memory ({g['vram_gb']} GB)"
    if g["kind"] == "apple":
        return round(ram * 0.65, 1), f"unified memory ({ram} GB, about 65% usable)"
    return round(ram * 0.7, 1), f"RAM ({ram} GB, about 70% usable)"


def recommend(info: dict) -> dict:
    """Largest tier that fits, and one tier lower. Always returns lines a person can read at a glance."""
    bud, where = budget(info)
    fits = [b for b, _ in TIERS if need_gb(b) <= bud]
    rec = fits[-1] if fits else None
    order = [b for b, _ in TIERS]
    lower = order[order.index(rec) - 1] if rec and order.index(rec) > 0 else None
    cpu_only = info["gpu"]["kind"] == "none"
    def line(b, label):
        note = ""
        if b == 3: note = " — testing only; a 3B model failed the engine's rules in my real test"
        return f"{label}: {b}B instruct, Q4_K_M — file ≈ {round(GB_PER_B * b, 1)} GB, needs ≈ {need_gb(b)} GB of {where.split(' (')[0]}{note}"
    lines = []
    if rec is None:
        lines.append(f"Not enough memory for a local model at the full 32k context ({bud} GB usable; the smallest tier needs ≈ {need_gb(3)} GB). "
                     "Use another computer on your network via Tailscale/Ollama, or add RAM.")
    else:
        lines.append(line(rec, "Recommended"))
        if lower: lines.append(line(lower, "One tier lower (faster, a little weaker)"))
        nxt = [b for b in order if b > rec]
        if nxt: lines.append(f"Next tier up ({nxt[0]}B) needs ≈ {need_gb(nxt[0])} GB; it can still run by spilling into RAM, but slowly.")
    if cpu_only:
        lines.append("No GPU detected: every turn is several model calls, so expect minutes per turn (a 3B model took about 15 minutes per turn on 4 CPU cores in my test). "
                     "A GPU, or another computer's GPU over Tailscale, makes play comfortable.")
    lines.append("Pick any recent instruct model of that size with a 32k+ context (for example the Qwen2.5-Instruct family, or a newer one); get its Q4_K_M .gguf file.")
    return {"budget_gb": bud, "budget_from": where, "recommended_b": rec, "lower_b": lower, "lines": lines}


def problems(info: dict) -> list[dict]:
    """What is missing, whether the program may install it without admin rights, and the exact command to do it yourself."""
    out = []
    if not info["python_ok"]:
        out.append({"id": "python", "label": f"Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+ (this is {info['python']})", "auto": False,
                    "manual": "Install Python 3.11 or newer from python.org (choose 'Install for me only' to avoid needing admin), then start the program again."})
    if not info["pyyaml"]:
        out.append({"id": "pyyaml", "label": "PyYAML (reads the world and save files)", "auto": True,
                    "manual": f'"{sys.executable}" -m pip install pyyaml'})
    runtime = info["ollama"] or info["lmstudio"]
    if not info["llama_cpp"] and not runtime:
        why = "" if info["compiler"] else " (no C++ compiler was found, so only a ready-made package will work; if none fits, use Ollama or LM Studio instead)"
        out.append({"id": "llama_cpp", "label": "llama-cpp-python (runs the AI model inside this program)" + why, "auto": True,
                    "manual": f'"{sys.executable}" -m pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu'})
    if not info["models"] and not runtime:
        out.append({"id": "model", "label": "an AI model file (.gguf)", "auto": False,
                    "manual": "Download a .gguf file and put it in the models/ folder (see the recommendation), or let the program fetch it from a direct https link to the .gguf file."})
    return out


def format_report(info: dict) -> str:
    g = info["gpu"]
    rows = [f"Computer: {info['os']} · {info['cpu_cores']} CPU cores · RAM {info['ram_gb']} GB ({info['ram_free_gb']} GB free) · disk free {info['disk_free_gb']} GB",
            f"Graphics: {g['name']}" + (f" · {g['vram_gb']} GB" if g["vram_gb"] else ""),
            f"Python: {info['python']} {'ok' if info['python_ok'] else '— too old'}" + (" (private environment)" if info["in_venv"] else ""),
            f"PyYAML: {'installed' if info['pyyaml'] else 'MISSING'} · llama-cpp-python: {'installed' if info['llama_cpp'] else 'missing'} · "
            f"C++ compiler: {info['compiler'] or 'none found'}",
            "Models in models/: " + (", ".join(f"{m['name']} ({m['gb']} GB)" for m in info["models"]) or "none"),
            f"Model servers running: Ollama {'yes' if info['ollama'] else 'no'} · LM Studio {'yes' if info['lmstudio'] else 'no'}"]
    rec = recommend(info)
    return "\n".join(rows + ["", "Recommendation:"] + ["  " + l for l in rec["lines"]])
