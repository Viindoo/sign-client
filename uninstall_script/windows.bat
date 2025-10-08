@echo off
REM Viindoo Sign Client - Windows Uninstall Script
REM This script removes the application and all associated files

echo === Viindoo Sign Client - Windows Uninstaller ===
echo This will remove Viindoo Sign Client and all associated files.
echo.

REM Ask for confirmation
set /p confirm="Are you sure you want to uninstall Viindoo Sign Client? (y/N): "
if /i not "%confirm%"=="y" (
    echo Uninstall cancelled.
    pause
    exit /b 0
)

echo Removing application files...

REM Remove desktop shortcut
if exist "%USERPROFILE%\Desktop\Viindoo Sign Client.lnk" (
    echo Removing desktop shortcut...
    del "%USERPROFILE%\Desktop\Viindoo Sign Client.lnk"
    echo ✓ Desktop shortcut removed
) else (
    echo Desktop shortcut not found
)

REM Remove start menu shortcut
if exist "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Viindoo Sign Client.lnk" (
    echo Removing start menu shortcut...
    del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Viindoo Sign Client.lnk"
    echo ✓ Start menu shortcut removed
) else (
    echo Start menu shortcut not found
)

REM Remove application data directory (optional)
set /p remove_data="Remove application data directory? (y/N): "
if /i "%remove_data%"=="y" (
    if exist "%USERPROFILE%\.viin_sign_client_data" (
        echo Removing application data directory...
        rmdir /s /q "%USERPROFILE%\.viin_sign_client_data"
        echo ✓ Application data directory removed
    ) else (
        echo Application data directory not found
    )
) else (
    echo Application data directory kept
)

REM Remove Python virtual environment (optional)
set /p remove_venv="Remove Python virtual environment? (y/N): "
if /i "%remove_venv%"=="y" (
    if exist "%~dp0..\.venv" (
        echo Removing Python virtual environment...
        rmdir /s /q "%~dp0..\.venv"
        echo ✓ Python virtual environment removed
    ) else (
        echo Python virtual environment not found
    )
) else (
    echo Python virtual environment kept
)

REM Remove Windows Registry entries (if any)
echo Checking for registry entries...
reg query "HKEY_CURRENT_USER\Software\Viindoo\SignClient" >nul 2>&1
if %errorlevel%==0 (
    echo Removing registry entries...
    reg delete "HKEY_CURRENT_USER\Software\Viindoo\SignClient" /f >nul 2>&1
    echo ✓ Registry entries removed
) else (
    echo No registry entries found
)

echo.
echo === Uninstall completed successfully! ===
echo.
echo The following items have been removed:
echo - Desktop shortcut
echo - Start menu shortcut
echo - Application data directory (if selected)
echo - Python virtual environment (if selected)
echo - Registry entries (if any)
echo.
echo Note: Python 3.10 and Microsoft Visual C++ are kept installed as they might be used by other applications.
echo If you want to remove them as well, you can uninstall them from:
echo - Microsoft Store (for Python 3.10)
echo - Add or Remove Programs (for Visual C++)
echo.
pause
