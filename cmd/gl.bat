@echo off
IF "%1" == "" git whatchanged
IF NOT "%1" == "" git whatchanged -p --since="2 weeks ago" -- %1
@echo on