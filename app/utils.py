import os
import subprocess
import sys

def get_abs_path(relative_path):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), relative_path))

def detect_python_version():
    """
    Detect available Python version (3.11+, 3.12+, 3.13+, or fallback to 3.10)
    Returns tuple (version_str, python_executable)
    """
    # Try versions from newest to oldest (3.13, 3.12, 3.11, 3.10)
    python_versions = ['3.13', '3.12', '3.11', '3.10']
    
    for version in python_versions:
        python_exe = f'python{version}'
        try:
            result = subprocess.run(
                [python_exe, '--version'],
                capture_output=True,
                text=True,
                timeout=2
            )
            if result.returncode == 0:
                return version, python_exe
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    
    # Fallback to system python3
    try:
        result = subprocess.run(
            ['python3', '--version'],
            capture_output=True,
            text=True,
            timeout=2
        )
        if result.returncode == 0:
            version_str = result.stdout.strip().split()[-1]  # e.g., "3.13.0"
            major_minor = '.'.join(version_str.split('.')[:2])  # e.g., "3.13"
            return major_minor, 'python3'
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    
    # Last resort: use current interpreter
    current_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    return current_version, sys.executable

# Detect Python version
_python_version, _python_executable = detect_python_version()

application_path = get_abs_path('..')
requirements_path = os.path.join(application_path, 'requirements.txt')
data_dir_path = os.path.join(application_path, 'data_dir')
python_venv_path = os.path.join(application_path, '.venv')

# Use detected Python version for venv path
if os.name == 'posix':
    python_venv_exec_path = os.path.join(python_venv_path, 'bin', 'python')
else:
    python_venv_exec_path = os.path.join(python_venv_path, 'Scripts', 'python.exe')

log_path = os.path.join(data_dir_path, 'log.txt')

def create_file(path):
    with open(path, 'w') as f:
        f.write('')
