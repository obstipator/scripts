@echo off
IF "%1" == "" explorer .
IF NOT "%1" == "" ( START /MIN cmd.exe /k "cde %1 && exp && exit")
@echo on