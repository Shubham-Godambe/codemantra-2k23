@echo off
REM CODEMANTRA 2K23 - Tree Enumeration Platform
REM Startup script for Windows

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║       CODEMANTRA 2K23 - Tree Enumeration MVP          ║
echo ║    AI-Based Forest Land Analysis Using Aerial Images   ║
echo ╚════════════════════════════════════════════════════════╝
echo.

cd /D "%~dp0"

echo [1/4] Checking virtual environment...
if not exist venv (
    echo ERROR: Virtual environment not found!
    echo Please run: python -m venv venv
    pause
    exit /b 1
)

echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/4] Starting FastAPI server...
echo.
echo Server starting on http://127.0.0.1:8000
echo Press Ctrl+C to stop the server
echo.

python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

pause
