@echo off
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0download.ps1"
if errorlevel 1 echo Download did not finish. Please send a screenshot of the error.
pause
