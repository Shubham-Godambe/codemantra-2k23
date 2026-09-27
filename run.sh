#!/bin/bash
# CODEMANTRA 2K23 - Tree Enumeration Platform
# Startup script for macOS/Linux

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║       CODEMANTRA 2K23 - Tree Enumeration MVP          ║"
echo "║    AI-Based Forest Land Analysis Using Aerial Images   ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

cd "$(dirname "$0")"

echo "[1/4] Checking virtual environment..."
if [ ! -d "venv" ]; then
    echo "ERROR: Virtual environment not found!"
    echo "Please run: python3 -m venv venv"
    exit 1
fi

echo "[2/4] Activating virtual environment..."
source venv/bin/activate

echo "[3/4] Starting FastAPI server..."
echo ""
echo "Server starting on http://127.0.0.1:8000"
echo "Press Ctrl+C to stop the server"
echo ""

python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
