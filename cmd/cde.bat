@echo off
"%~dp0../inc/cde.py" "%1" > "%~dp0../temp/dirTemp.txt"
set /p myvar= < "%~dp0../temp/dirTemp.txt"
echo. > "%~dp0../temp/dirTemp.txt"
cd /d %myvar%
@echo on