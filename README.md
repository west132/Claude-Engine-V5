# Claude Engine V5 — the AI GM as software

NEW ENGINE v5.0 as a local app: code does the dice, numbers, state, GM-Δ chain and saves; a local language model (a `.gguf` you
download once and drop in `models/`) judges, narrates and checks, following the engine's own text.

- **Install & play:** [INSTALL.md](INSTALL.md)
- **How it works / what is code vs model:** [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **Try without a model:** `python -m gmhost serve --demo` · **verify install:** `python -m gmhost check`
- **Tests:** `pip install pytest && pytest`

`engine/` holds the five original files unchanged. `examples/` holds four ready worlds; `tests/data/ashfall/` is a real 120-round campaign used as the regression test.
