@echo off
echo ================================
echo XRP Dashboard Quick Start
echo ================================
echo.

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH"
    pause
    exit
)

echo.
echo Installing required libraries...
pip install requests

echo.
echo Running dashboard update...
python xrp_dashboard_updater.py

echo.
echo Opening dashboard in browser...
start xrp_dashboard.html

echo.
echo ================================
echo Dashboard is now running!
echo Press Ctrl+C to stop updates
echo ================================
echo.

python xrp_dashboard_updater.py --continuous 15
