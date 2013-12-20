

@"%~dp0../inc/paste.exe" > "%~dp0../temp/js2phpIn.txt"
@node "%~dp0../inc/js2php.js" %~dp0 | clip
@echo Copied to clipboard.
