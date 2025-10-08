import os
import platform
import stat
import sys

# Add parent directory to path to import app.utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import utils

def is_ubuntu():
    """Check if running on Ubuntu"""
    return 'ubuntu' in platform.version().lower()

def create_python_venv():
    """Create Python virtual environment and install dependencies"""
    if os.path.exists(utils.python_venv_path):
        print('✅ Python virtual environment already exists, skipping...')
        return
    
    print('Creating Python virtual environment...')
    os.system(f"python3.10 -m venv '{utils.python_venv_path}'")
    
    print('Upgrading pip and setuptools...')
    os.system(f"{utils.python_venv_exec_path} -m pip install --upgrade pip setuptools")
    
    print('Installing Python dependencies...')
    os.system(f"{utils.python_venv_exec_path} -m pip install -r '{utils.requirements_path}'")
    
    print('✅ Python virtual environment created successfully!')

def create_desktop_app():
    """Create desktop entry for Ubuntu"""
    if not is_ubuntu():
        print('Not running on Ubuntu, skipping desktop entry creation...')
        return
    
    print('Creating desktop entry for Ubuntu...')
    script = utils.get_abs_path('../main.py')
    exec_cmd = f'{utils.python_venv_exec_path} {script}'

    icon_path = utils.get_abs_path('../app/assets/icon.ico')
    if not os.path.exists(icon_path):
        print('⚠️  Warning: Icon file not found at app/assets/icon.ico')
        icon_path = ''

    desktop_content = f"""[Desktop Entry]
Version=1.0
Name=Viindoo Sign Client
Exec={exec_cmd}
Icon={icon_path}
Terminal=false
Type=Application
Categories=Utility;
"""
    desktop_file = '/usr/share/applications/viin_sign.desktop'
    with open(desktop_file, 'w') as file:
        file.write(desktop_content)
    os.chmod(desktop_file, 0o644)
    
    print('✅ Desktop entry created successfully!')

def make_datadir():
    """Create data directory and log file"""
    if os.path.exists(utils.data_dir_path):
        print('✅ Data directory already exists, skipping...')
        return
    
    print('Creating data directory...')
    os.makedirs(utils.data_dir_path, exist_ok=True)
    utils.create_file(utils.log_path)
    
    # Set appropriate permissions for Unix-like systems
    if os.name == 'posix':
        os.chmod(utils.data_dir_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        os.chmod(utils.log_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    
    print('✅ Data directory created successfully!')

def main():
    """Main installation function"""
    print("=== Viindoo Sign Client - Linux Python Installer ===")
    print(f"Running on: {platform.system()} {platform.release()}")
    print()
    
    try:
        # Create Python virtual environment
        create_python_venv()
        print()
        
        # Create desktop app (Ubuntu only)
        create_desktop_app()
        print()
        
        # Create data directory
        make_datadir()
        print()
        
        print("=== Python installer completed successfully! ===")
        print()
        print("You can now run Viindoo Sign Client:")
        if is_ubuntu():
            print("- From Applications menu (Ubuntu)")
        print("- Command line: ./bin.sh")
        print("- Direct: python3.10 main.py")
        print()
        
    except Exception as e:
        print(f"❌ Error during installation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
