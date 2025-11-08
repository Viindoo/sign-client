# PowerShell script to create desktop and start menu shortcuts

$ErrorActionPreference = "Stop"

Write-Host "=== Creating Shortcuts ===" -ForegroundColor Cyan
Write-Host ""

$WshShell = New-Object -comObject WScript.Shell

# Get the application path
$AppPath = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$VBSPath = Join-Path $AppPath "run_hidden.vbs"

# Create Desktop shortcut
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$DesktopShortcutPath = "$DesktopPath\Viindoo Sign Client.lnk"

try {
    $Shortcut = $WshShell.CreateShortcut($DesktopShortcutPath)
    $Shortcut.TargetPath = "wscript.exe"
    $Shortcut.Arguments = """$VBSPath"""
    $Shortcut.WorkingDirectory = $AppPath
    $Shortcut.IconLocation = "$AppPath\app\assets\icon.ico"
    $Shortcut.Description = "Viindoo Sign Client"
    $Shortcut.Save()
    Write-Host "Desktop shortcut created successfully!" -ForegroundColor Green
} catch {
    Write-Host "Failed to create Desktop shortcut: $_" -ForegroundColor Red
    exit 1
}

# Create Start Menu shortcut
$StartMenuPath = [Environment]::GetFolderPath("StartMenu")
$ProgramsPath = Join-Path $StartMenuPath "Programs"

# Ensure Programs directory exists
if (-not (Test-Path $ProgramsPath)) {
    New-Item -ItemType Directory -Path $ProgramsPath -Force | Out-Null
}

$StartMenuShortcutPath = "$ProgramsPath\Viindoo Sign Client.lnk"

try {
    $Shortcut = $WshShell.CreateShortcut($StartMenuShortcutPath)
    $Shortcut.TargetPath = "wscript.exe"
    $Shortcut.Arguments = """$VBSPath"""
    $Shortcut.WorkingDirectory = $AppPath
    $Shortcut.IconLocation = "$AppPath\app\assets\icon.ico"
    $Shortcut.Description = "Viindoo Sign Client"
    $Shortcut.Save()
    Write-Host "Start Menu shortcut created successfully!" -ForegroundColor Green
} catch {
    Write-Host "Failed to create Start Menu shortcut: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== Shortcuts created successfully! ===" -ForegroundColor Green
