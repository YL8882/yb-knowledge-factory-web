@echo off
chcp 65001 >nul
cd /d "%~dp0"
start "YB Knowledge Factory Server" cmd /k python run.py
timeout /t 3 /nobreak >nul
start http://127.0.0.1:8000
