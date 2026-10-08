# Copyright (c) 2026 West132.WL. All rights reserved.
"""Local web server (stdlib only). Binds to 127.0.0.1; long operations stream progress as SSE."""
from __future__ import annotations
import hmac
import ipaddress
import json
import mimetypes
import re
import shutil
import subprocess
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs, unquote

from .app import App
from .campaign import CampaignError
from .config import Config
from .llm import LLMError
from .turn import TurnError

WEB = Path(__file__).resolve().parents[1] / "web"
_NAME = re.compile(r"^[A-Za-z0-9_\-]{1,40}$")


def host_allowed(host_header: str, extra=()) -> bool:
    """DNS-rebinding guard: accept only names that really mean this machine or its tailnet."""
    h = (host_header or "").strip().lower()
    if h.startswith("["):                       # [::1]:8765
        h = h[1:].split("]")[0]
    elif h.count(":") == 1:
        h = h.split(":")[0]
    if h in ("127.0.0.1", "localhost", "::1") or h.endswith(".ts.net") or h in {x.lower() for x in extra}:
        return True
    try:
        return ipaddress.ip_address(h) in ipaddress.ip_network("100.64.0.0/10")      # Tailscale addresses
    except ValueError:
        return False


def tailscale_ip() -> str | None:
    exe = shutil.which("tailscale")
    if exe:
        try:
            out = subprocess.run([exe, "ip", "-4"], capture_output=True, text=True, timeout=5).stdout.split()
            if out: return out[0]
        except Exception:
            pass
    try:                                         # fall back to scanning this machine's addresses
        import socket
        for info in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET):
            if host_allowed(info[4][0]) and info[4][0] != "127.0.0.1": return info[4][0]
    except Exception:
        pass
    return None


def make_handler(app: App):
    class H(BaseHTTPRequestHandler):
        server_version = "GMHost/0.1"

        def log_message(self, *a): pass

        # ---- plumbing ---------------------------------------------------------------------
        def _host_ok(self) -> bool:
            return host_allowed(self.headers.get("Host"), app.cfg.server.allowed_hosts)

        def _auth_ok(self) -> bool:
            tok = app.cfg.server.token
            if not tok: return True
            for part in (self.headers.get("Cookie") or "").split(";"):
                k, _, v = part.strip().partition("=")
                if k == "gm_token" and hmac.compare_digest(v, tok): return True
            return False

        def _json(self, obj, code=200):
            data = json.dumps(obj, ensure_ascii=False).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(data)

        def _body(self) -> dict:
            n = int(self.headers.get("Content-Length") or 0)
            if n > 6_000_000: raise CampaignError("request too large")
            return json.loads(self.rfile.read(n).decode("utf-8")) if n else {}

        def _stream(self, fn):
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            def emit(ev):
                self.wfile.write(("data: " + json.dumps(ev, ensure_ascii=False) + "\n\n").encode("utf-8"))
                self.wfile.flush()
            try:
                emit({"type": "done", "payload": fn(emit)})
            except (CampaignError, TurnError, LLMError, ValueError, KeyError) as e:
                emit({"type": "error", "message": str(e)})
            except (BrokenPipeError, ConnectionResetError):
                pass
            except Exception as e:
                emit({"type": "error", "message": f"{type(e).__name__}: {e}"})

        def _guard(self, fn):
            try:
                fn()
            except (CampaignError, TurnError, LLMError, ValueError, KeyError) as e:
                self._json({"error": str(e)}, 400)
            except Exception as e:
                self._json({"error": f"{type(e).__name__}: {e}"}, 500)

        # ---- GET ---------------------------------------------------------------------------
        def do_GET(self):
            if not self._host_ok(): return self._json({"error": "bad host"}, 403)
            u = urlparse(self.path)
            q = parse_qs(u.query)
            path = unquote(u.path)
            tok = app.cfg.server.token
            if tok and q.get("token", [""])[0] and hmac.compare_digest(q["token"][0], tok):
                self.send_response(302)
                self.send_header("Set-Cookie", f"gm_token={tok}; HttpOnly; SameSite=Strict; Path=/; Max-Age=31536000")
                self.send_header("Location", "/"); self.end_headers(); return
            if not self._auth_ok():
                data = b"<!doctype html><meta name=viewport content='width=device-width'><body style='font:16px system-ui;padding:2rem'>This server needs its access token. Open the link with <code>?token=...</code> once."
                self.send_response(401); self.send_header("Content-Type", "text/html; charset=utf-8"); self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data); return
            if path == "/api/info": return self._guard(lambda: self._json({**app.info(), "examples": [e["id"] for e in app.examples()]}))
            if path == "/api/example":
                return self._guard(lambda: self._json(next(e for e in app.examples() if e["id"] == q.get("id", [""])[0])))
            if path == "/api/campaign": return self._guard(lambda: self._json(app.snapshot()))
            if path == "/api/gmlog": return self._guard(lambda: self._json({"text": app.gm_log(q.get("spoilers", ["0"])[0] == "1")}))
            if path.startswith("/api/download/"):
                def dl():
                    name = path.rsplit("/", 1)[1]
                    p = app.background_file() if name == "background" else app.save_file(name)
                    data = p.read_bytes()
                    self.send_response(200)
                    self.send_header("Content-Type", "text/markdown; charset=utf-8")
                    self.send_header("Content-Disposition", f'attachment; filename="{p.name}"')
                    self.send_header("Content-Length", str(len(data)))
                    self.end_headers(); self.wfile.write(data)
                return self._guard(dl)
            if path == "/favicon.ico":
                self.send_response(204); self.end_headers(); return
            rel = "index.html" if path in ("/", "") else path.lstrip("/")
            f = (WEB / rel).resolve()
            if WEB.resolve() not in f.parents and f != WEB.resolve() / "index.html" or not f.is_file():
                return self._json({"error": "not found"}, 404)
            data = f.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", (mimetypes.guess_type(f.name)[0] or "text/plain") + "; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers(); self.wfile.write(data)

        # ---- POST --------------------------------------------------------------------------
        def do_POST(self):
            if not self._host_ok() or self.headers.get("X-GM") != "1" or not self._auth_ok():
                return self._json({"error": "forbidden"}, 403)
            path = urlparse(self.path).path
            try:
                b = self._body()
            except Exception as e:
                return self._json({"error": f"bad request: {e}"}, 400)
            if path == "/api/unassigned":
                return self._guard(lambda: self._json({"fields": app.unassigned(b["background"])}))
            if path == "/api/create":
                def go(emit):
                    if not _NAME.match(b.get("name", "")): raise CampaignError("campaign name: letters, digits, _ and -")
                    app.create(b["name"], b.get("background"), b.get("premise"), b.get("language"), b.get("profile"), b.get("encoding"), emit, b.get("fill"))
                    return {"name": b["name"]}
                return self._stream(go)
            if path == "/api/open":
                return self._guard(lambda: (app.open(b["name"]), self._json(app.snapshot())))
            if path == "/api/import":
                def imp():
                    if not _NAME.match(b.get("name", "")): raise CampaignError("campaign name: letters, digits, _ and -")
                    app.import_save(b["name"], b["save"], b["background"]); self._json(app.snapshot())
                return self._guard(imp)
            if path == "/api/opening": return self._stream(lambda emit: app.opening(emit))
            if path == "/api/play": return self._stream(lambda emit: app.play(b.get("text", ""), emit))
            if path == "/api/save": return self._stream(lambda emit: app.save(emit))
            if path == "/api/continue_unsaved": return self._guard(lambda: (app.continue_unsaved(), self._json({"ok": True})))
            if path == "/api/options": return self._guard(lambda: (app.set_options(b.get("profile"), b.get("language")), self._json(app.snapshot())))
            if path == "/api/reload_model": return self._guard(lambda: (app.load_model(), self._json(app.info())))
            self._json({"error": "not found"}, 404)

    return H


def serve(cfg: Config, port: int | None = None, open_browser: bool = True, app: App | None = None,
          tailscale: bool | None = None, host: str | None = None):
    app = app or App(cfg)
    port = port or cfg.server.port
    print("Storyteller — Copyright (c) 2026 West132.WL. All rights reserved.")
    hosts = [host or cfg.server.host]
    if tailscale or (tailscale is None and cfg.server.tailscale):
        ts = tailscale_ip()
        if ts: hosts.append(ts)
        else: print("NOTE: --tailscale given but no Tailscale address found (is Tailscale running?). Serving locally only.")
    servers = [ThreadingHTTPServer((h, port), make_handler(app)) for h in dict.fromkeys(hosts)]
    for h in dict.fromkeys(hosts):
        print(f"GM host running at http://{h}:{port}/")
    if len(servers) > 1 and not cfg.server.token:
        print("NOTE: anyone on your tailnet can open this. Set [server] token in config.toml to require an access token.")
    if cfg.server.token:
        print(f"Access token is on: open  http://<address>:{port}/?token={cfg.server.token}  once on each device.")
    if app.model_error:
        print("NOTE: no model is loaded yet:\n  " + app.model_error.replace("\n", "\n  "))
    if open_browser:
        threading.Timer(0.8, lambda: webbrowser.open(f"http://127.0.0.1:{port}/" + (f"?token={cfg.server.token}" if cfg.server.token else ""))).start()
    for extra in servers[1:]:
        threading.Thread(target=extra.serve_forever, daemon=True).start()
    try:
        servers[0].serve_forever()
    except KeyboardInterrupt:
        print("\nbye")
    return servers[0]
