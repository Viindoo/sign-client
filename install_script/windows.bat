@echo off
setlocal enabledelayedexpansion
REM Viindoo Sign Client - Windows Installation Script
REM This script checks for prerequisites and sets up the application

echo === Viindoo Sign Client - Windows Installer ===
echo.
echo This script will check for prerequisites and set up the application.
echo.
echo Prerequisites required:
echo   - Python 3.10
echo   - Microsoft C++ Build Tools
echo.

REM Function to find Python 3.10 command (python or python3.10)
echo Checking for Python 3.10...
set PYTHON_CMD=

REM Try python3.10 first - check if it actually runs (not just alias)
python3.10 --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    REM Check if it's actually Python 3.10 and not a redirect
    for /f "tokens=*" %%v in ('python3.10 --version 2^>^&1') do (
        echo %%v | findstr /R "Python 3\.10\." >nul
        if !ERRORLEVEL! EQU 0 (
            REM Verify it can actually execute Python code
            python3.10 -c "import sys; exit(0 if sys.version_info[:2] == (3, 10) else 1)" >nul 2>&1
            if !ERRORLEVEL! EQU 0 (
                set PYTHON_CMD=python3.10
                echo [OK] Found Python 3.10 ^(python3.10^)
                goto :python_found
            )
        )
    )
)

REM Try python - check if it actually runs (not just alias)
python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    REM Check if it's actually Python 3.10 and not a redirect to Store
    for /f "tokens=*" %%v in ('python --version 2^>^&1') do (
        echo %%v | findstr /R "Python 3\.10\." >nul
        if !ERRORLEVEL! EQU 0 (
            REM Verify it can actually execute Python code (not Store redirect)
            python -c "import sys; exit(0 if sys.version_info[:2] == (3, 10) else 1)" >nul 2>&1
            if !ERRORLEVEL! EQU 0 (
                set PYTHON_CMD=python
                echo [OK] Found Python 3.10 ^(python^)
                goto :python_found
            )
        )
    )
)

REM Python 3.10 not found
echo [ERROR] Python 3.10 is not installed.
echo.
echo Please install Python 3.10 manually:
echo   1. Download from: https://www.python.org/downloads/release/python-31011/
echo   2. Run the installer ^(64-bit^)
echo   3. IMPORTANT: Check "Add Python to PATH" during installation
echo   4. Restart your terminal after installation
echo   5. Run this script again
echo.
pause
exit /b 1

:python_found
if not defined PYTHON_CMD (
    echo [ERROR] Error: Python 3.10 command not found.
    pause
    exit /b 1
)

REM Check for C++ Build Tools
echo.
echo Checking for Microsoft C++ Build Tools...
set CPP_TOOLS_FOUND=0

REM Check if vswhere.exe exists (Visual Studio Installer)
if exist "%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe" (
    REM Use vswhere to check for C++ Build Tools
    "%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe" -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        set CPP_TOOLS_FOUND=1
        echo [OK] Found Microsoft C++ Build Tools
    )
)

if !CPP_TOOLS_FOUND! EQU 0 (
    echo [ERROR] Microsoft C++ Build Tools is not installed.
    echo.
    echo This is required for building some Python dependencies.
    echo.
    echo Please install Microsoft C++ Build Tools:
    echo   1. Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
    echo   2. Download "Build Tools"
    echo   3. During installation, select:
    echo      - Desktop development with C++ ^(workload^)
    echo      - MSVC v143 - VS 2022 C++ x64/x86 build tools ^(component^)
    echo      - Windows 11 SDK ^(latest version^)
    echo   4. After installation, run this script again
    echo.
    pause
    exit /b 1
)

echo.
echo Running Python installer to setup application...
%PYTHON_CMD% windows_installer.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [OK] Python installer completed successfully!
    echo.
    echo Creating desktop and start menu shortcuts...
    powershell -ExecutionPolicy Bypass -File "%~dp0create_shortcuts.ps1"
    
    if %ERRORLEVEL% EQU 0 (
        echo [OK] Shortcuts created successfully!
        echo.
        echo === Installation completed successfully! ===
        echo.
        echo You can now run Viindoo Sign Client from:
        echo - Desktop shortcut
        echo - Start Menu
        echo - Command line: %PYTHON_CMD% main.py
        echo.
    ) else (
        echo [ERROR] Error creating shortcuts. You can still run the application manually.
    )
) else (
    echo [ERROR] Python installer failed. Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo For more information, visit: https://github.com/Viindoo/sign-client
pause
