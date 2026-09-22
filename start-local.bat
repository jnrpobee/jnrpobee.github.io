@echo off
cd /d %~dp0
py serve.py 8001 || python serve.py 8001
pause
