@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Run scripts\setup.ps1 first.
  pause
  exit /b 1
)
echo Open http://127.0.0.1:8765 in your browser. Press Ctrl+C to stop.
".venv\Scripts\python.exe" run_workbench.py
pause
