
@ git diff | egrep "\+.*?(console\.log|var_dump)" > "%~dp0../temp/gitDumpTemp.txt"
@ set gitdump=
@ set /p gitdump= < "%~dp0../temp/gitDumpTemp.txt"
@if not defined  gitdump (echo "all good") else (
  start cmd /k "less -p ""(console\.log^|var_dump)"" ""%~dp0../temp/gitDumpTemp.txt"" && echo. > ""%~dp0../temp/gitDumpTemp.txt"" && exit"
)
@ git diff