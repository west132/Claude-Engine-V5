@echo off
REM One-click launcher (Windows). First run creates a private Python environment and installs what is needed.
cd /d "%~dp0"
if not exist .venv (
  echo First run: creating environment ^(needs internet once^)...
  py -3 -m venv .venv || python -m venv .venv
  call .venv\Scripts\activate.bat
  python -m pip install --upgrade pip >nul
  pip install pyyaml
  pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu || echo !! llama-cpp-python could not be installed. You can still use Ollama / LM Studio ^(see INSTALL.md^).
) else (
  call .venv\Scripts\activate.bat
)
python -m gmhost %*
pause
