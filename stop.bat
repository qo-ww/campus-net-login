@echo off
echo Stopping campus network auto-login...
taskkill /f /im pythonw.exe 2>nul
echo Stopped.
pause