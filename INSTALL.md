# Install manual

You need: a computer with **Python 3.11+**, a **model file** (downloaded once), and about 12–40 GB of free disk/RAM depending on the model.
After the one-time setup the game runs fully offline.

## Do I need administrator rights?
**No.** Nothing is installed into Windows/macOS/Linux itself. Everything lives in this folder: the program, your stories and saves, the model file, and a private Python environment (`.venv`) that `start.sh` / `start.bat` create on first run. To remove it all, delete the folder.

The one condition: **Python 3.11 or newer must already be on the computer** (the launcher uses it). If it is not, install Python for the current user only (the python.org installer has an “Install for me only / no admin” option), or ask whoever manages the machine. After that, the first run downloads two small packages into `.venv` (needs internet once), with no admin step. If `llama-cpp-python` has no ready-made package for your system it needs a C++ compiler, which usually does need setup — in that case use Option B below (Ollama or LM Studio, which normally install per-user).

## First run: the setup assistant
The first time you start the program it **checks your computer first** (system, RAM, graphics card, disk, Python, the packages, any model file or running Ollama / LM Studio), then goes through what is missing **one item at a time and asks you**:
- *Install it for me* — the program runs the install (only things that need no admin rights), or
- *I'll do it myself* — it shows the exact command to copy, or
- *Skip for now.*

Things that would change your system (installing Python, a C++ compiler, GPU drivers) are never done for you; you get instructions instead. You can run it again at any time: `python -m gmhost setup` (add `--check` to only look, `--auto` to accept every no-admin install). The same screen is in the app under **⋯ → Computer check & setup**, where you can also paste a direct `.gguf` download link and let the program fetch the model (it resumes interrupted downloads and prints the file's SHA-256 so you can compare it with the one on the download page).

## 1. Get the program
Download or clone this repository. Everything (engine files, app, web page) is inside it.

## 2. Download a model and put it in `models/`
Download **one** instruction-tuned model in **GGUF** format and place the file in the `models/` folder.

What the model must be good at: following long rules, producing valid JSON, writing prose in your game language.
The engine rules alone take ~12k tokens of context, so pick a model with a context window of **32k or more**.

| Your computer | Recommended | One tier lower (faster, a little weaker) |
|---|---|---|
| 8 GB RAM, no GPU | 3B (testing only) | — (too little memory for more) |
| 16 GB RAM, no GPU | 7B | 3B |
| 32 GB RAM, no GPU | 14B | 7B |
| 64 GB RAM, no GPU | 32B | 14B |
| NVIDIA 8–16 GB VRAM | 7B | 3B |
| NVIDIA 24 GB VRAM | 14B | 7B |
| NVIDIA 48 GB VRAM | 32B | 14B |
| Apple Silicon 16 GB / 32 GB / 64 GB | 7B / 14B / 32B | 3B / 7B / 14B |

"B" is billions of parameters; use an instruct model's `Q4_K_M` file with a 32k+ context. The numbers assume the full 32k context (the rules alone take ~12k tokens). **The program works this out for you**: `python -m gmhost setup` (or *Computer check & setup* in the app's menu) reads your RAM, GPU and disk and prints the recommended size and the one below it. Without a GPU every turn takes minutes; a 3B model is only good for checking that things run (in my real test it broke the engine's rules).

Look for GGUF files on Hugging Face (search “<model name> GGUF”). I could not download or run any model in the environment this
software was built in, so no specific model has been validated by me — run `python -m gmhost check --load` (step 4) with yours.
Bigger is more reliable at the referee role; the checker and the code-enforced rules catch many, not all, mistakes.

## 3. Start it
- **Windows:** double-click `start.bat`
- **macOS / Linux:** run `./start.sh`

The first run creates a private Python environment and installs `pyyaml` and `llama-cpp-python` (needs internet once). Your browser opens
at http://127.0.0.1:8765. If it says “no model loaded”, the message tells you what is missing; add the file and press *reload the model*.

*If llama-cpp-python will not install* (it needs a C++ compiler when no prebuilt wheel fits, and GPU builds need extra flags — see the
llama-cpp-python project page), use **Option B**.

### Option B — use Ollama / LM Studio / llama-server instead
Install and start one of them, load a model there, then copy `config.example.toml` to `config.toml` and set:
```toml
[model]
backend  = "openai"
base_url = "http://127.0.0.1:11434/v1"   # Ollama; LM Studio is http://127.0.0.1:1234/v1
model    = "name-of-your-model"
n_ctx    = 32768                          # set the same context size in that program
```

### GPU
`n_gpu_layers = -1` (default) offloads everything that fits. For NVIDIA/Apple GPUs install the matching llama-cpp-python build
(see its documentation) inside `.venv`. CPU-only works but each turn takes noticeably longer (a turn is several model calls).

## 4. Check the installation
```
python -m gmhost check            # python, packages, engine files, offline 10-round self-test (no model needed)
python -m gmhost check --load     # also loads your model and asks it for schema-constrained JSON
python -m gmhost serve --demo     # click through the whole app with a stand-in instead of a model
```
(`start.sh`/`start.bat` pass their arguments through: `./start.sh check --load`.)

## 5. Play
1. **New** → name, game language, output length (full / lite), then a world:
   an example, **your own filled BACKGROUND file**, or *Generate from idea* (the model fills the template; the program validates it).
2. Type what you do. The program rolls dice, keeps HP/XP/time/inventory, writes the engine's lines, and the model narrates.
3. A **checkpoint save** is written automatically every 10 rounds (`campaigns/<name>/saves/save_<name>_R<N>.md`) and play pauses for
   you. *Settings* lets you download the newest save and the BACKGROUND. Both together are your campaign.
4. **Import** (Load → Import) accepts saves made by the chat version of the engine, plus their BACKGROUND file.

Spoilers: saves contain the hidden world state (that is how the engine persists it). Choose *base64* for “Hidden state in saves” when
creating a campaign if you do not want to read it by accident. The *Engine log* hides hidden entries unless you tick the spoiler box.

## Troubleshooting
- **“model context … too small”** – raise `n_ctx` in `config.toml` (and your server) to 32768 or more. The rules are never trimmed.
- **Turns fail with “malformed tool calls”** – the model is too weak or not instruct-tuned; try a larger one.
- **Slow turns** – use *lite*, a smaller model, or a GPU build.
- **Port in use** – change `[server] port`.

## Your own worlds and saves
- `examples/` ships four ready worlds (Tarnstead, Ashfall, Cyberpunk RED, Last Scion). Worlds with `[UNASSIGNED]` fields (name, age, weapon…) ask you to fill them in before play starts.
- **Import** an older save with its BACKGROUND. The importer repairs what the engine's field rules forbid (prose inside numbers/dates, missing item points, NPCs without required fields set to `unknown`) and lists every repair; nothing is silent.
- Audit any save: `python -m gmhost audit <save.md> <BACKGROUND.md>`.


## Use it from your phone or another computer (Tailscale)
The model and all game state stay on your desktop; the phone is just a screen.
1. Install Tailscale on the desktop and on the phone/other computer, signed in to the same account. Check the phone shows the desktop as connected.
2. On the desktop start the app so it also listens on the Tailscale address:
   - `./start.sh serve --tailscale` (Windows: `start.bat serve --tailscale`), or set `tailscale = true` under `[server]` in `config.toml`.
   - The console prints the addresses, e.g. `http://100.101.102.103:8765/`.
3. On the phone open that address in the browser (or `http://<desktop-name>:8765/` if MagicDNS is on). Add it to the home screen for an app-like icon.

Notes
- Traffic between your devices is already encrypted by Tailscale. The app only accepts connections addressed to localhost, a Tailscale address (100.64.0.0/10) or a `*.ts.net` name; other devices on your Wi-Fi cannot reach it.
- **Anyone on your tailnet can open it** (including devices you have shared). To require a password-like token, set `token = "something-long"` under `[server]`, then open `http://<address>:8765/?token=something-long` once on each device (a cookie remembers it).
- Prefer HTTPS? Run `tailscale serve --bg 8765` on the desktop and open the `https://<desktop-name>.<tailnet>.ts.net` address it prints; the app still listens only on localhost.
- The desktop must stay on and awake while you play, and one story is played at a time.


## Language

The first time you open the app it asks for a language: **English** or **简体中文**. Your last choice is remembered in `prefs.json` (delete it to be asked again) and is preselected for new stories. You can change it any time in *Settings*. The command-line setup assistant (`python -m gmhost setup`) is English only.
