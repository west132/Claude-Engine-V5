@echo off
REM Copyright (c) 2026 West132.WL. All rights reserved.
REM Launcher (Windows). Asks before installing anything; nothing outside this folder is changed.
cd /d "%~dp0"
set PYCMD=
py -3 -c "import sys; sys.exit(0 if sys.version_info>=(3,11) else 1)" >nul 2>&1 && set PYCMD=py -3
if "%PYCMD%"=="" python -c "import sys; sys.exit(0 if sys.version_info>=(3,11) else 1)" >nul 2>&1 && set PYCMD=python
if "%PYCMD%"=="" (
  echo This program needs Python 3.11 or newer and it was not found.
  echo Install it from python.org ^(choose "Install for me only" - no admin needed^), then run this again.
  pause & exit /b 1
)
if not exist .venv (
  echo First run. The program needs a small Python package ^(PyYAML^); the setup then asks how you want to run the AI.
  echo They go into a private folder ^(.venv^) inside this directory: no administrator rights, nothing changes in your system.
  echo   1^) Let the program set it up for me ^(needs internet once^)
  echo   2^) I will do it myself ^(show me the commands^)
  set /p CHOICE=Choose 1 or 2 [1]: 
  if "%CHOICE%"=="2" (
    echo.
    echo Run these, then start this launcher again:
    echo   %PYCMD% -m venv .venv
    echo   .venv\Scripts\activate
    echo   pip install pyyaml
    echo   python -m gmhost setup
    pause & exit /b 0
  )
  %PYCMD% -m venv .venv
  call .venv\Scripts\activate.bat
  pip install --disable-pip-version-check pyyaml
  python -m gmhost setup --first-run
) else (
  call .venv\Scripts\activate.bat
)
python -m gmhost %*
pause
