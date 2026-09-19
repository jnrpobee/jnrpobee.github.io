@echo off
cd /d %~dp0
py serve.py 8000 || python serve.py 8000
pause
