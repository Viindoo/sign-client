@echo off
REM Viindoo Sign Client - Windows Installation Script
REM This script automatically installs Python 3.10 and dependencies for Windows

echo === Viindoo Sign Client - Windows Installer ===
echo Installing dependencies for Windows...
echo.

REM Check if Python 3.10 is installed
python3.10 --version >nul 2>&1

if %ERRORLEVEL% EQU 0 (
    echo ✅ Python 3.10 is already installed.
    echo.
    echo Running Python installer to setup application...
    python3.10 windows_installer.py
    
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo ✅ Python installer completed successfully!
        echo.
        echo Creating desktop and start menu shortcuts...
        powershell -ExecutionPolicy Bypass -File "%~dp0create_shortcuts.ps1"
        
        if %ERRORLEVEL% EQU 0 (
            echo ✅ Shortcuts created successfully!
            echo.
            echo === Installation completed successfully! ===
            echo.
            echo You can now run Viindoo Sign Client from:
            echo - Desktop shortcut
            echo - Start Menu
            echo - Command line: python3.10 main.py
            echo.
        ) else (
            echo ❌ Error creating shortcuts. You can still run the application manually.
        )
    ) else (
        echo ❌ Python installer failed. Please check the error messages above.
        pause
        exit /b 1
    )
) else (
    echo ❌ Python 3.10 is not installed.
    echo.
    echo Please install Python 3.10 first:
    echo 1. Open Microsoft Store
    echo 2. Search for "python3.10" and install it
    echo 3. Download and install Microsoft Visual C++ 14 from:
    echo    https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist
    echo 4. Run this script again
    echo.
    pause
    exit /b 1
)

echo.
echo For more information, visit: https://github.com/Viindoo/sign-client
pause
