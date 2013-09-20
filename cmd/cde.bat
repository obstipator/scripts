@echo off
"C:/scripts/inc/cde.py" "%1" > "C:/scripts/temp/dirTemp.txt"
set /p myvar= < C:/scripts/temp/dirTemp.txt
echo. > "C:/scripts/temp/dirTemp.txt"
cd /d %myvar%
@echo on