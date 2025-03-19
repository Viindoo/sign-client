$WshShell = New-Object -comObject WScript.Shell

# Get the application path
$AppPath = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$VBSPath = Join-Path $AppPath "run_hidden.vbs"

# Create Desktop shortcut
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$Shortcut = $WshShell.CreateShortcut("$DesktopPath\Viindoo Sign Client.lnk")
$Shortcut.TargetPath = "wscript.exe"
$Shortcut.Arguments = """$VBSPath"""
$Shortcut.WorkingDirectory = $AppPath
$Shortcut.IconLocation = "$AppPath\app\assets\icon.ico"
$Shortcut.Description = "Viindoo Sign Client"
$Shortcut.Save()

# Create Start Menu shortcut
$StartMenuPath = [Environment]::GetFolderPath("StartMenu")
$ProgramsPath = Join-Path $StartMenuPath "Programs"
$Shortcut = $WshShell.CreateShortcut("$ProgramsPath\Viindoo Sign Client.lnk")
$Shortcut.TargetPath = "wscript.exe"
$Shortcut.Arguments = """$VBSPath"""
$Shortcut.WorkingDirectory = $AppPath
$Shortcut.IconLocation = "$AppPath\app\assets\icon.ico"
$Shortcut.Description = "Viindoo Sign Client"
$Shortcut.Save()

Write-Host "Shortcuts created successfully!"
