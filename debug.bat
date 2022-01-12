@echo off
:: Windows launch example
:: This should be moved to the root of your project, and the path should be updated below

:start
cls
python start.py -l debug
PAUSE
goto :start