import os
import platform
import stat
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import utils


def is_ubuntu():
    return 'ubuntu' in platform.version().lower()


def create_python_venv():
    if os.path.exists(utils.python_venv_path):
        print('python venv already exists, ignore.')
        return
    os.system(f"python3.10 -m venv '{utils.python_venv_path}'")
    os.system(f"{utils.python_venv_exec_path} -m pip install --upgrade pip setuptools")
    os.system(f"{utils.python_venv_exec_path} -m pip install -r '{utils.requirements_path}'")


def create_desktop_app():
    script = utils.get_abs_path('../main.py')
    exec_cmd = f'{utils.python_venv_exec_path} {script}'

    icon_path = utils.get_abs_path('../app/assets/icon.ico')
    if not os.path.exists(icon_path):
        print('Warning: Icon file not found at app/assets/icon.ico')
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
if is_ubuntu():
    create_desktop_app()
make_datadir()
print('install successfully')
