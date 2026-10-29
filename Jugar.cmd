@echo off
cd /d "%~dp0"
where py >nul 2>nul
if not errorlevel 1 (
  py -3 tools\serve_game.py
  goto :end
)
if exist "%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" (
  "%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" tools\serve_game.py
  goto :end
)
where python >nul 2>nul
if not errorlevel 1 (
  python tools\serve_game.py
  goto :end
)
echo Necesitas Python 3 o abrir EcoGame.capx en Construct y pulsar F5.
:end
pause
