import os
import platform
import stat
import sys
import subprocess
import shutil

# Add parent directory to path to import app.utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import utils

def is_macos():
    """Check if running on macOS"""
    return platform.system() == 'Darwin'

def create_python_venv():
    """Create Python virtual environment and install dependencies"""
    if os.path.exists(utils.python_venv_path):
        print('Python venv already exists, skipping...')
        return
    
    print('Creating Python virtual environment...')
    os.system(f"python3.10 -m venv '{utils.python_venv_path}'")
    
    print('Upgrading pip and setuptools...')
    os.system(f"{utils.python_venv_exec_path} -m pip install --upgrade pip setuptools")
    
    print('Installing Python dependencies...')
    os.system(f"{utils.python_venv_exec_path} -m pip install -r '{utils.requirements_path}'")
    
    print('Python virtual environment created successfully!')

def create_app_bundle():
    """Create macOS App Bundle (.app) for Applications folder"""
    if not is_macos():
        print('Not running on macOS, skipping App Bundle creation...')
        return
    
    app_name = "Viindoo Sign Client.app"
    app_path = f"/Applications/{app_name}"
    
    print(f'Creating macOS App Bundle: {app_name}...')
    
    # Remove existing app if it exists
    if os.path.exists(app_path):
        print(f'{app_name} already exists, removing...')
        shutil.rmtree(app_path)
    
    # Create App Bundle structure
    os.makedirs(f"{app_path}/Contents/MacOS", exist_ok=True)
    os.makedirs(f"{app_path}/Contents/Resources", exist_ok=True)
    
    # Create Info.plist
    info_plist_content = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>viin_sign_client</string>
    <key>CFBundleIdentifier</key>
    <string>com.viindoo.signclient</string>
    <key>CFBundleName</key>
    <string>Viindoo Sign Client</string>
    <key>CFBundleDisplayName</key>
    <string>Viindoo Sign Client</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleIconFile</key>
    <string>icon.icns</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.15</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>"""
    
    with open(f"{app_path}/Contents/Info.plist", 'w') as f:
        f.write(info_plist_content)
    
    # Create executable script
    script_path = utils.get_abs_path('../main.py')
    app_dir = os.path.dirname(script_path)
    
    exec_script_content = f"""#!/bin/bash
# Viindoo Sign Client Launcher

# Change to application directory
cd "{app_dir}"

# Activate virtual environment and run application
"{utils.python_venv_exec_path}" "{script_path}"
"""
    
    exec_script_path = f"{app_path}/Contents/MacOS/viin_sign_client"
    with open(exec_script_path, 'w') as f:
        f.write(exec_script_content)
    
    # Make executable
    os.chmod(exec_script_path, 0o755)
    
    # Copy icon if it exists
    icon_path = utils.get_abs_path('../app/assets/icon.ico')
    if os.path.exists(icon_path):
        print('Copying application icon...')
        # For now, just copy the .ico file (could be converted to .icns later)
        shutil.copy2(icon_path, f"{app_path}/Contents/Resources/icon.icns")
    else:
        print('Warning: Application icon not found at app/assets/icon.ico')
    
    print(f'App Bundle created successfully at: {app_path}')

def create_launchd_plist():
    """Create LaunchAgent plist for auto-start (optional)"""
    if not is_macos():
        return
    
    plist_name = "com.viindoo.signclient.plist"
    plist_path = os.path.expanduser(f"~/Library/LaunchAgents/{plist_name}")
    
    # Create LaunchAgents directory if it doesn't exist
    os.makedirs(os.path.dirname(plist_path), exist_ok=True)
    
    script_path = utils.get_abs_path('../main.py')
    app_dir = os.path.dirname(script_path)
    
    plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.viindoo.signclient</string>
    <key>ProgramArguments</key>
    <array>
        <string>{utils.python_venv_exec_path}</string>
        <string>{script_path}</string>
    </array>
    <key>WorkingDirectory</key>
    <string>{app_dir}</string>
    <key>RunAtLoad</key>
    <false/>
    <key>KeepAlive</key>
    <false/>
</dict>
</plist>"""
    
    with open(plist_path, 'w') as f:
        f.write(plist_content)
    
    print(f'LaunchAgent plist created at: {plist_path}')
    print('Note: To enable auto-start, run: launchctl load ~/Library/LaunchAgents/com.viindoo.signclient.plist')

def make_datadir():
    """Create data directory and log file"""
    if os.path.exists(utils.data_dir_path):
        print('Data directory already exists, skipping...')
        return
    
    print('Creating data directory...')
    os.makedirs(utils.data_dir_path, exist_ok=True)
    utils.create_file(utils.log_path)
    
    # Set appropriate permissions
    if os.name == 'posix':
        os.chmod(utils.data_dir_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        os.chmod(utils.log_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    
    print('Data directory created successfully!')

def create_symlink():
    """Create symlink in /usr/local/bin for easy command line access"""
    if not is_macos():
        return
    
    symlink_path = "/usr/local/bin/viin-sign-client"
    script_path = utils.get_abs_path('../main.py')
    
    try:
        # Remove existing symlink if it exists
        if os.path.exists(symlink_path) or os.path.islink(symlink_path):
            os.unlink(symlink_path)
        
        # Create new symlink
        os.symlink(script_path, symlink_path)
        print(f'Symlink created: {symlink_path} -> {script_path}')
        print('You can now run the application with: viin-sign-client')
        
    except PermissionError:
        print('Warning: Could not create symlink in /usr/local/bin (permission denied)')
        print('You can still run the application using ./bin.sh or from Applications folder')

def main():
    """Main installation function"""
    print("=== Viindoo Sign Client - macOS Python Installer ===")
    print(f"Running on: {platform.system()} {platform.release()}")
    print()
    
    try:
        # Create Python virtual environment
        create_python_venv()
        print()
        
        # Create data directory
        make_datadir()
        print()
        
        # Create macOS App Bundle
        if is_macos():
            create_app_bundle()
            print()
            
            # Create LaunchAgent plist (optional)
            create_launchd_plist()
            print()
            
            # Create symlink for command line access
            create_symlink()
            print()
        
        print("=== Installation completed successfully! ===")
        print()
        print("You can now:")
        print("1. Run from Applications folder: 'Viindoo Sign Client'")
        print("2. Run from command line: ./bin.sh")
        if is_macos():
            print("3. Run from command line: viin-sign-client")
        print()
        print("To uninstall, simply delete the application folder and remove:")
        print("- /Applications/Viindoo Sign Client.app")
        print("- ~/Library/LaunchAgents/com.viindoo.signclient.plist")
        print("- /usr/local/bin/viin-sign-client")
        
    except Exception as e:
        print(f"Error during installation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
