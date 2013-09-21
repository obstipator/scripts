@echo off
"%~dp0../inc/pngout.exe" "%1" "%~dp0../temp/pngoutTemp.png" /y
( printf "data:image/png;base64," && ( %~dp0../inc/base64.exe -i "%~dp0../temp/pngoutTemp.png" -n 0 ) ) | "%~dp0../inc/clip.exe"
echo. 
echo copied to clipboard
@echo on