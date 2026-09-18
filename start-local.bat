@echo off
cd /d %~dp0
echo Portfolio running at http://localhost:8000
py -m http.server 8000
pause
