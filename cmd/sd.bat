@if "%1"=="" (
@svn diff -r PREV | TortoiseUDiff /p /title:"HERE IS THE DIFF LATEST" ) else (
@svn diff -r %1 | TortoiseUDiff /p /title:"HERE IS THE DIFF OF %1" )