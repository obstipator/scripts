@ svn diff | egrep "\+.*?(console\.log|var_dump)" > "%~dp0../temp/svnDumpTemp.txt"
@ set svndump=
@ set /p svndump= < "%~dp0../temp/svnDumpTemp.txt"
@if not defined  svndump (echo "all good") else (
  start cmd /k "less -p ""(console\.log^|var_dump)"" ""%~dp0../temp/svnDumpTemp.txt"" && echo. > ""%~dp0../temp/svnDumpTemp.txt"" && exit"
)
@ svn diff | less