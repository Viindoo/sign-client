@echo off
setlocal enabledelayedexpansion

echo === Viindoo Sign Client - Windows Installer ===
echo Checking for Python 3.10 or newer...
echo.

set "PYTHON_EXE="
for %%P in (python python3 python3.13 python3.12 python3.11 python3.10) do (
    %%P -c "import sys; exit(0 if sys.version_info >= (3,10) else 1)" >nul 2>&1
    if !ERRORLEVEL! EQU 0 (
        set "PYTHON_EXE=%%P"
        goto found_python
    )
)

REM Not found — show user-friendly installation guide
if "%PYTHON_EXE%"=="" (
    echo ❌ No supported Python version found (3.10+).
    echo.
    echo Please install Python 3.10 or newer first using one of the following methods:
    echo.
    echo Method 1: Install from Microsoft Store (Recommended)
    echo   1. Open Microsoft Store
    echo   2. Search for "Python 3"
    echo   3. Install the Python version you want (3.10+)
    echo.
    echo Method 2: Download from python.org
    echo   1. Download Python 3.10+ from https://www.python.org/downloads/
    echo   2. IMPORTANT: During installation, CHECK "Add python.exe to PATH"
    echo.
    echo After installing Python:
    echo   1. Install Microsoft Visual C++ 14 from:
    echo      https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist
    echo   2. Run this script again
    echo.
    pause
    exit /b 1
)

:found_python
echo ✅ Found Python: %PYTHON_EXE%
echo Running installer...
echo.

call %PYTHON_EXE% windows_installer.py
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Installation completed successfully!
    echo.
    echo Creating shortcuts...
    powershell -ExecutionPolicy Bypass -File "%~dp0create_shortcuts.ps1"
) else (
    echo.
    echo ❌ Python installer failed. Please check the error messages above.
)

echo.
echo For more information, visit: https://github.com/Viindoo/sign-client
pause
