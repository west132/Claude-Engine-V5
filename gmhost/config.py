"""Settings. Everything has a default so the app starts with no config file."""
from __future__ import annotations
import os
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(os.environ.get("GMHOST_HOME") or Path(__file__).resolve().parents[1])


@dataclass
class ModelCfg:
    backend: str = "auto"          # auto | llama_cpp | openai | mock
    path: str = ""                 # blank = first .gguf found in models/
    n_ctx: int = 32768
    n_gpu_layers: int = -1         # -1 = offload everything the GPU can hold
    n_threads: int = 0             # 0 = let llama.cpp choose
    max_new_tokens: int = 2048
    base_url: str = "http://127.0.0.1:11434/v1"
    model: str = ""
    api_key: str = ""


@dataclass
class GameCfg:
    language: str = "en"
    profile: str = "full"          # full | lite  (engine §2.2 PROFILE)
    encoding: str = "plain"        # plain | b64 | rot13 (engine §8.1 ENCODING)
    max_referee_steps: int = 28
    narration_retries: int = 2
    history_turns: int = 6


@dataclass
class ServerCfg:
    host: str = "127.0.0.1"
    port: int = 8765


@dataclass
class Config:
    model: ModelCfg = field(default_factory=ModelCfg)
    game: GameCfg = field(default_factory=GameCfg)
    server: ServerCfg = field(default_factory=ServerCfg)
    root: Path = ROOT

    @property
    def engine_dir(self) -> Path: return self.root / "engine"
    @property
    def models_dir(self) -> Path: return self.root / "models"
    @property
    def campaigns_dir(self) -> Path: return self.root / "campaigns"


def load_config(path: Path | None = None) -> Config:
    cfg = Config()
    p = path or ROOT / "config.toml"
    if p.exists():
        raw = tomllib.loads(p.read_text(encoding="utf-8"))
        for section, obj in (("model", cfg.model), ("game", cfg.game), ("server", cfg.server)):
            for k, v in (raw.get(section) or {}).items():
                if hasattr(obj, k):
                    setattr(obj, k, v)
    if os.environ.get("GMHOST_BACKEND"):
        cfg.model.backend = os.environ["GMHOST_BACKEND"]
    return cfg
