@echo off
title Campus Auto Login Setup
cd /d "%~dp0"
echo ========================================
echo   Campus Net Auto Login - Setup
echo ========================================
echo.
echo Checking Python...

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo Python not found! Please install Python first:
    echo 1. Visit https://www.python.org/downloads/
    echo 2. Download and install, MUST check "Add Python to PATH"
    echo 3. Then re-run this setup
    echo.
    start https://www.python.org/downloads/
    pause
    exit /b
)

echo Python OK!
echo.
echo Installing dependencies (may take a few minutes)...
echo.

pip install requests -q
pip install playwright -q
echo.
echo Installing browser (this step is slow)...
playwright install chromium

echo.
echo ========================================
echo   Setup complete!
echo.
echo   Next steps:
echo   1. Edit config.txt with your student ID
echo   2. Double-click oneclick_start.bat
echo ========================================
pause