import os

def get_abs_path(relative_path):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), relative_path))

application_path = get_abs_path('..')
requirements_path = os.path.join(application_path, 'requirements.txt')
data_dir_path = os.path.join(application_path, 'data_dir')
python_venv_path = os.path.join(application_path, '.venv')
if os.name == 'posix':
    python_venv_exec_path = os.path.join(python_venv_path, 'bin', 'python3.10')
else:
    python_venv_exec_path = os.path.join(python_venv_path, 'Scripts', 'python.exe')
log_path = os.path.join(data_dir_path, 'log.txt')

def create_file(path):
    with open(path, 'w') as f:
        f.write('')
