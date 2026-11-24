@echo off
chcp 65001 >nul
cd /d "%~dp0.."
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" LAB_4_lis.py
) else (
    python LAB_4_lis.py
)
if errorlevel 1 pause
