import os
import stat
import sys
import platform

# Add parent directory to path to import app.utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import utils

def create_python_venv():
    """Create Python virtual environment and install dependencies"""
    if os.path.exists(utils.python_venv_path):
        print('✅ Python virtual environment already exists, skipping...')
        return
    
    print('Creating Python virtual environment...')
    os.system(f"python3.10 -m venv {utils.python_venv_path}")
    
    print('Upgrading pip and setuptools...')
    os.system(f"{utils.python_venv_exec_path} -m pip install --upgrade pip setuptools")
    
    print('Installing Python dependencies...')
    os.system(f"{utils.python_venv_exec_path} -m pip install -r {utils.requirements_path}")
    
    print('✅ Python virtual environment created successfully!')

def create_desktop_app():
    """Desktop app creation is handled by PowerShell script"""
    print('Desktop shortcuts will be created by PowerShell script...')

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
    print("=== Viindoo Sign Client - Windows Python Installer ===")
    print(f"Running on: {platform.system()} {platform.release()}")
    print()
    
    try:
        # Create Python virtual environment
        create_python_venv()
        print()
        
        # Create desktop app (handled by PowerShell)
        create_desktop_app()
        print()
        
        # Create data directory
        make_datadir()
        print()
        
        print("=== Python installer completed successfully! ===")
        print()
        print("Next steps:")
        print("1. Desktop and Start Menu shortcuts will be created")
        print("2. You can run the application from shortcuts or command line")
        print()
        
    except Exception as e:
        print(f"❌ Error during installation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
