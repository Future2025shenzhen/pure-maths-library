@echo off
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0open-library.ps1"
if errorlevel 1 (
 echo Could not open papers. Please send a screenshot of the error.
 pause
)
