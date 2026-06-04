@echo off
cd /d "C:\Users\??\Desktop\???????"
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\create_shortcut.vbs"
echo sLinkFile = oWS.SpecialFolders("Startup") ^& "\CampusAutoLogin.lnk" >> "%TEMP%\create_shortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\create_shortcut.vbs"
echo oLink.TargetPath = "%CD%\run_hidden.vbs" >> "%TEMP%\create_shortcut.vbs"
echo oLink.WorkingDirectory = "%CD%" >> "%TEMP%\create_shortcut.vbs"
echo oLink.Description = "Campus Network Auto Login" >> "%TEMP%\create_shortcut.vbs"
echo oLink.Save >> "%TEMP%\create_shortcut.vbs"
cscript //nologo "%TEMP%\create_shortcut.vbs"
del "%TEMP%\create_shortcut.vbs"
echo.
echo Done! Added to startup.
pause