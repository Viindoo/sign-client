import os
import stat
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import utils


def create_python_venv():
    if os.path.exists(utils.python_venv_path):
        print('python venv already exists, ignore.')
        return
    os.system(f"python3.10 -m venv {utils.python_venv_path}")
    os.system(f"{utils.python_venv_exec_path} -m pip install --upgrade pip setuptools")
    os.system(f"{utils.python_venv_exec_path} -m pip install -r {utils.requirements_path}")


def create_desktop_app():
    pass


def make_datadir():
    if os.path.exists(utils.data_dir_path):
        print('data dir already exists, ignore.')
        return
    else:
        os.mkdir(utils.data_dir_path)
        utils.create_file(utils.log_path)
        if os.name == 'posix':
            os.chmod(utils.data_dir_path,  stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
            os.chmod(utils.log_path,  stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)


create_python_venv()
create_desktop_app()
make_datadir()
print('install successfully')
