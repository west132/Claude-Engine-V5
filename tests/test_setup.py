# Copyright (c) 2026 West132.WL. All rights reserved.
import hashlib
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest

from gmhost import setup_wizard, sysinfo


def info(ram, gpu="none", vram=0, **kw):
    base = {"os": "T", "cpu_cores": 8, "ram_gb": ram, "ram_free_gb": ram, "disk_free_gb": 100, "gpu": {"kind": gpu, "name": "x", "vram_gb": vram},
            "python": "3.12.0", "python_ok": True, "in_venv": True, "pyyaml": True, "llama_cpp": True, "compiler": None, "cmake": False,
            "models": [], "ollama": False, "lmstudio": False}
    base.update(kw); return base


@pytest.mark.parametrize("args,rec,lower", [
    ((4,), None, None), ((8,), 3, None), ((16,), 7, 3), ((32,), 14, 7), ((64,), 32, 14), ((128,), 70, 32),
    ((32, "nvidia", 12), 7, 3), ((32, "nvidia", 24), 14, 7), ((64, "nvidia", 48), 32, 14), ((32, "apple"), 14, 7)])
def test_recommended_tier_and_one_lower(args, rec, lower):
    r = sysinfo.recommend(info(*args))
    assert (r["recommended_b"], r["lower_b"]) == (rec, lower)
    if rec: assert r["lines"][0].startswith("Recommended") and (not lower or r["lines"][1].startswith("One tier lower"))


def test_cpu_only_warns_about_speed_and_gpu_does_not():
    assert any("minutes per turn" in l for l in sysinfo.recommend(info(32))["lines"])
    assert not any("minutes per turn" in l for l in sysinfo.recommend(info(32, "nvidia", 24))["lines"])


def test_problems_say_what_can_be_automated():
    p = {x["id"]: x for x in sysinfo.problems(info(16, pyyaml=False, llama_cpp=False))}
    assert p["pyyaml"]["auto"] and p["llama_cpp"]["auto"] and not p["model"]["auto"]
    assert "pip install" in p["pyyaml"]["manual"] and "whl/cpu" in p["llama_cpp"]["manual"]
    assert not sysinfo.problems(info(16, models=[{"name": "m.gguf", "gb": 4}]))
    assert not [x for x in sysinfo.problems(info(16, llama_cpp=False, models=[], ollama=True))]       # a running Ollama is enough
    old = sysinfo.problems(info(16, python_ok=False, python="3.9.1"))
    assert old[0]["id"] == "python" and not old[0]["auto"]


def test_wizard_asks_and_respects_each_choice(tmp_path, monkeypatch):
    monkeypatch.setattr(sysinfo, "gather", lambda root: info(16, pyyaml=True, llama_cpp=False, models=[]))
    installed = []
    monkeypatch.setattr(setup_wizard, "pip_install", lambda item, say=print: installed.append(item) or False)
    out = []
    answers = iter(["2", ""])                        # llama_cpp: "I'll do it myself"; model: just press Enter
    code = setup_wizard.run(tmp_path, ask=lambda q: next(answers), say=out.append)
    text = "\n".join(out)
    assert installed == [] and "pip install llama-cpp-python" in text and code == 1
    answers = iter(["1", ""])                        # now: install it for me
    setup_wizard.run(tmp_path, ask=lambda q: next(answers), say=out.append)
    assert installed == ["llama_cpp"]


def test_check_only_changes_nothing(tmp_path, monkeypatch):
    monkeypatch.setattr(sysinfo, "gather", lambda root: info(16, llama_cpp=False))
    monkeypatch.setattr(setup_wizard, "pip_install", lambda *a, **k: pytest.fail("must not install"))
    assert setup_wizard.run(tmp_path, check_only=True, say=lambda t: None) == 1


class _Serve(BaseHTTPRequestHandler):
    DATA = bytes(range(256)) * 4096                      # 1 MiB
    def log_message(self, *a): pass
    def do_GET(self):
        rng = self.headers.get("Range")
        start = int(rng.split("=")[1].split("-")[0]) if rng else 0
        body = self.DATA[start:]
        self.send_response(206 if rng else 200); self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)


def test_download_resumes_and_verifies_sha(tmp_path):
    srv = ThreadingHTTPServer(("127.0.0.1", 0), _Serve); threading.Thread(target=srv.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{srv.server_address[1]}/tiny.gguf"
    want = hashlib.sha256(_Serve.DATA).hexdigest()
    (tmp_path / "tiny.gguf.part").write_bytes(_Serve.DATA[:300000])             # an interrupted earlier download
    dest = setup_wizard.download(url, tmp_path, say=lambda t: None, sha256="sha256:" + want)
    assert dest.read_bytes() == _Serve.DATA and not (tmp_path / "tiny.gguf.part").exists()
    with pytest.raises(ValueError, match="does not match"):
        setup_wizard.download(url, tmp_path, say=lambda t: None, sha256="0" * 64)
    assert not (tmp_path / "tiny.gguf").exists()
    with pytest.raises(ValueError, match="gguf"):
        setup_wizard.download("http://x/y.zip", tmp_path)
    srv.shutdown()
