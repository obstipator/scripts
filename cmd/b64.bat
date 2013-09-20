@echo off
"C:/scripts/inc/pngout.exe" "%1" "C:/scripts/temp/pngoutTemp.png" /y
( printf "data:image/png;base64," && ( C:/scripts/inc/base64.exe -i "C:/scripts/temp/pngoutTemp.png" -n 0 ) ) | "C:/scripts/inc/clip.exe"
echo. 
echo copied to clipboard
@echo on