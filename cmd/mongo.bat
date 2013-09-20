@echo off
START /MIN "mongo" "C:\Program Files (x86)\mongo\bin\mongod" --dbpath="C:\Program Files (x86)\mongo\data"
echo Started Mongo (minified)
@echo on