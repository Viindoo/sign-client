@echo off
python3.10 --version >nul 2>&1

if %ERRORLEVEL% EQU 0 (
    echo Python 3.10 is installed. Running windows_installer.py to setup ...
    python3.10 windows_installer.py

    echo Creating shortcuts...
    powershell -ExecutionPolicy Bypass -File "%~dp0create_shortcuts.ps1"
) else (
    echo Python 3.10 is not installed. You need install python3.10 through Microsoft Store.
)
