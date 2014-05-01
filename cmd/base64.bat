@echo off
printf "data:image/" && (identify "%1" | gawk "{printf tolower($2)}") && printf ";base64," && ( %~dp0../inc/base64.exe -i "%1" -n 0 ) | "%~dp0../inc/clip.exe"
echo. 
echo copied to clipboard
@echo on