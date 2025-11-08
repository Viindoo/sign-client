import os
import stat
import sys
import platform
import subprocess

# Add parent directory to path to import app.utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import utils

def check_python_version():
    """Check if Python version is exactly 3.10"""
    if sys.version_info.major != 3 or sys.version_info.minor != 10:
        raise Exception(f"Python 3.10 is required, but found {sys.version_info.major}.{sys.version_info.minor}")

def create_python_venv():
    """Create Python virtual environment and install dependencies"""
    if os.path.exists(utils.python_venv_path):
        print('✅ Python virtual environment already exists, skipping...')
        return
    
    python_cmd = sys.executable
    print(f'Using Python command: {python_cmd}')
    
    # Normalize paths to handle spaces correctly
    python_venv_path = os.path.normpath(utils.python_venv_path)
    python_venv_exec_path = os.path.normpath(utils.python_venv_exec_path)
    requirements_path = os.path.normpath(utils.requirements_path)
    
    print('Creating Python virtual environment...')
    # Use subprocess.run() instead of os.system() to handle paths with spaces correctly
    result = subprocess.run(
        [python_cmd, '-m', 'venv', python_venv_path],
        check=False,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        error_msg = result.stderr.strip() if result.stderr else result.stdout.strip()
        raise Exception(f"Failed to create virtual environment. Exit code: {result.returncode}\nError: {error_msg}")
    
    # Verify venv was created successfully
    if not os.path.exists(python_venv_exec_path):
        raise Exception(f"Virtual environment created but python executable not found at: {python_venv_exec_path}")
    
    print('Upgrading pip and setuptools...')
    result = subprocess.run(
        [python_venv_exec_path, '-m', 'pip', 'install', '--upgrade', 'pip', 'setuptools'],
        check=False,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        error_msg = result.stderr.strip() if result.stderr else result.stdout.strip()
        raise Exception(f"Failed to upgrade pip and setuptools. Exit code: {result.returncode}\nError: {error_msg}")
    
    print('Installing Python dependencies...')
    result = subprocess.run(
        [python_venv_exec_path, '-m', 'pip', 'install', '-r', requirements_path],
        check=False,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        error_msg = result.stderr.strip() if result.stderr else result.stdout.strip()
        raise Exception(f"Failed to install dependencies. Exit code: {result.returncode}\nError: {error_msg}")
    
    print('✅ Python virtual environment created successfully!')

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

    check_python_version()

    try:
        # Create Python virtual environment
        create_python_venv()
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
