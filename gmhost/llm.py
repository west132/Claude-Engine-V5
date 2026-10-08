"""Model backends. The rest of the app only sees `Backend.chat()`.

llama_cpp  loads a .gguf from models/ in-process (nothing else to install or run)
openai     talks to any OpenAI-compatible server: Ollama, LM Studio, llama-server, vLLM
scripted   returns queued replies; used by the tests and the --demo mode
"""
from __future__ import annotations
import json
import threading
import urllib.error
import urllib.request
from pathlib import Path
from typing import Callable

from .config import Config
from .textutil import est_tokens, strip_think


class LLMError(Exception):
    pass


class Backend:
    name = "base"
    n_ctx = 8192

    def chat(self, messages: list[dict], *, max_tokens: int = 1024, temperature: float = 0.3,
             schema: dict | None = None, on_token: Callable[[str], None] | None = None) -> str:
        raise NotImplementedError

    def count(self, text: str) -> int:
        return est_tokens(text)


def find_model(cfg: Config) -> Path:
    if cfg.model.path:
        p = Path(cfg.model.path)
        p = p if p.is_absolute() else cfg.root / p
        if not p.exists():
            raise LLMError(f"model file not found: {p}")
        return p
    found = sorted(f for f in cfg.models_dir.glob("**/*.gguf") if "mmproj" not in f.name.lower())
    if not found:
        raise LLMError(f"no .gguf model found in {cfg.models_dir}. Download one and put it there "
                       "(see INSTALL.md), or point config.toml at an Ollama / LM Studio server.")
    return found[0]


class LlamaCppBackend(Backend):
    name = "llama_cpp"

    def __init__(self, cfg: Config):
        try:
            from llama_cpp import Llama
        except ImportError as e:
            raise LLMError("llama-cpp-python is not installed (see INSTALL.md), or use the "
                           "OpenAI-compatible backend") from e
        self.path = find_model(cfg)
        self.n_ctx = cfg.model.n_ctx
        self._lock = threading.Lock()
        kw = dict(model_path=str(self.path), n_ctx=self.n_ctx, n_gpu_layers=cfg.model.n_gpu_layers,
                  verbose=False)
        if cfg.model.n_threads:
            kw["n_threads"] = cfg.model.n_threads
        self.llm = Llama(**kw)

    def count(self, text: str) -> int:
        try:
            return len(self.llm.tokenize(text.encode("utf-8"), add_bos=False))
        except Exception:
            return est_tokens(text)

    def chat(self, messages, *, max_tokens=1024, temperature=0.3, schema=None, on_token=None):
        kw = dict(messages=messages, max_tokens=max_tokens, temperature=temperature)
        if schema is not None:
            kw["response_format"] = {"type": "json_object", "schema": schema}
        with self._lock:
            if on_token:
                out = []
                for chunk in self.llm.create_chat_completion(stream=True, **kw):
                    piece = chunk["choices"][0]["delta"].get("content") or ""
                    if piece:
                        out.append(piece); on_token(piece)
                return strip_think("".join(out))
            r = self.llm.create_chat_completion(**kw)
            return strip_think(r["choices"][0]["message"]["content"] or "")


class OpenAICompatBackend(Backend):
    name = "openai"

    def __init__(self, cfg: Config):
        self.base = cfg.model.base_url.rstrip("/")
        self.model = cfg.model.model
        self.key = cfg.model.api_key
        self.n_ctx = cfg.model.n_ctx
        self._schema_mode = "json_schema"      # degrades to json_object, then to none

    def _post(self, payload: dict, stream: bool):
        req = urllib.request.Request(
            self.base + "/chat/completions", data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json",
                     **({"Authorization": f"Bearer {self.key}"} if self.key else {})})
        return urllib.request.urlopen(req, timeout=600)

    def chat(self, messages, *, max_tokens=1024, temperature=0.3, schema=None, on_token=None):
        while True:
            payload = {"model": self.model, "messages": messages, "max_tokens": max_tokens,
                       "temperature": temperature, "stream": bool(on_token)}
            if schema is not None and self._schema_mode == "json_schema":
                payload["response_format"] = {"type": "json_schema",
                                              "json_schema": {"name": "step", "schema": schema}}
            elif schema is not None and self._schema_mode == "json_object":
                payload["response_format"] = {"type": "json_object"}
            try:
                resp = self._post(payload, bool(on_token))
            except urllib.error.HTTPError as e:
                body = e.read().decode("utf-8", "replace")[:300]
                if e.code in (400, 422) and schema is not None and self._schema_mode != "none":
                    self._schema_mode = "json_object" if self._schema_mode == "json_schema" else "none"
                    continue
                raise LLMError(f"model server error {e.code}: {body}")
            except urllib.error.URLError as e:
                raise LLMError(f"cannot reach the model server at {self.base}: {e.reason}")
            if on_token:
                out = []
                for raw in resp:
                    line = raw.decode("utf-8", "replace").strip()
                    if not line.startswith("data:") or line.endswith("[DONE]"):
                        continue
                    try:
                        piece = json.loads(line[5:])["choices"][0]["delta"].get("content") or ""
                    except Exception:
                        continue
                    if piece:
                        out.append(piece); on_token(piece)
                return strip_think("".join(out))
            data = json.loads(resp.read().decode("utf-8"))
            return strip_think(data["choices"][0]["message"]["content"] or "")


class ScriptedBackend(Backend):
    """Replies from a queue (or a callable(messages, schema) -> str). Records every call."""
    name = "scripted"

    def __init__(self, replies=None, n_ctx: int = 32768):
        self.replies = replies if replies is not None else []
        self.n_ctx = n_ctx
        self.calls: list[dict] = []

    def chat(self, messages, *, max_tokens=1024, temperature=0.3, schema=None, on_token=None):
        self.calls.append({"messages": messages, "schema": schema})
        if callable(self.replies):
            out = self.replies(messages, schema)
        else:
            if not self.replies:
                raise LLMError("scripted backend ran out of replies")
            out = self.replies.pop(0)
        if not isinstance(out, str):
            out = json.dumps(out, ensure_ascii=False)
        if on_token:
            on_token(out)
        return out


def make_backend(cfg: Config) -> Backend:
    kind = cfg.model.backend
    if kind == "mock":
        from .demo import DemoBackend
        return DemoBackend()
    if kind == "openai":
        return OpenAICompatBackend(cfg)
    if kind == "llama_cpp":
        return LlamaCppBackend(cfg)
    # auto: a .gguf in models/ wins; otherwise try the local server address
    if any(cfg.models_dir.glob("**/*.gguf")):
        return LlamaCppBackend(cfg)
    if cfg.model.model:
        return OpenAICompatBackend(cfg)
    raise LLMError("no model configured. Put a .gguf file in the models/ folder "
                   "(see INSTALL.md), or set [model] backend/model in config.toml.")
