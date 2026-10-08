"""Local web server (stdlib only). Binds to 127.0.0.1; long operations stream progress as SSE."""
from __future__ import annotations
import json
import mimetypes
import re
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


def make_handler(app: App):
    class H(BaseHTTPRequestHandler):
        server_version = "GMHost/0.1"

        def log_message(self, *a): pass

        # ---- plumbing ---------------------------------------------------------------------
        def _host_ok(self) -> bool:
            host = (self.headers.get("Host") or "").split(":")[0]
            return host in ("127.0.0.1", "localhost", "[::1]", "::1")

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
            if not self._host_ok() or self.headers.get("X-GM") != "1":
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


def serve(cfg: Config, port: int | None = None, open_browser: bool = True, app: App | None = None):
    app = app or App(cfg)
    port = port or cfg.server.port
    httpd = ThreadingHTTPServer((cfg.server.host, port), make_handler(app))
    url = f"http://{cfg.server.host}:{port}/"
    print(f"GM host running at {url}")
    if app.model_error:
        print("NOTE: no model is loaded yet:\n  " + app.model_error.replace("\n", "\n  "))
    if open_browser:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nbye")
    return httpd
