@echo off
cd /d "%~dp0"
echo ================================
echo   Campus Network Auto Login
echo ================================
echo.
echo [1] Diagnostic Mode (show browser)
echo [2] Background Mode (silent)
echo [0] Stop
echo ================================
set /p choice=Select (0/1/2): 

if "%choice%"=="1" (
    echo.
    echo Starting diagnostic mode...
    python CampusNetwork.py --show
    pause
) else if "%choice%"=="2" (
    echo.
    echo Starting background mode...
    start "" /B pythonw CampusNetwork.py
    echo Running in background!
    timeout /t 2 >nul
) else if "%choice%"=="0" (
    call stop.bat
) else (
    echo Invalid choice
    pause
)
