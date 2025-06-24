@echo off
echo Starting Optimized Game Launcher...
cd /d "%~dp0"
python start_launcher.py
if errorlevel 1 (
    echo.
    echo Failed to start launcher. Trying alternative method...
    python optimized_launcher.py
)
pause
