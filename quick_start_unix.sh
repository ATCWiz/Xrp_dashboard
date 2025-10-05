#!/bin/bash

echo "================================"
echo "XRP Dashboard Quick Start"
echo "================================"
echo

echo "Checking Python installation..."
if ! command -v python3 &> /dev/null
then
    echo "ERROR: Python3 not found!"
    echo "Install with: brew install python3 (Mac)"
    echo "Or: sudo apt install python3 (Linux)"
    exit 1
fi

python3 --version

echo
echo "Installing required libraries..."
pip3 install requests

echo
echo "Running dashboard update..."
python3 xrp_dashboard_updater.py

echo
echo "Opening dashboard in browser..."
open xrp_dashboard.html || xdg-open xrp_dashboard.html

echo
echo "================================"
echo "Dashboard is now running!"
echo "Press Ctrl+C to stop updates"
echo "================================"
echo

python3 xrp_dashboard_updater.py --continuous 15
