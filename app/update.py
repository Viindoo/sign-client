import os
import shutil
import zipfile

import requests
import logging
from requests.exceptions import ConnectionError, HTTPError

import version
from app import utils

_logger = logging.getLogger(__name__)

UPDATE_URL = 'https://api.github.com/repos/Viindoo/sign-client/releases/latest'
EXCLUDE_IN_BACKUP_RESTORE = ['data_dir', '.venv', '.git', '__pycache__']


class Updater:
    def __init__(self, data=None):
        data = data or {}
        self.update_url = data.get('update_url', UPDATE_URL)

    def get_updating_data(self):
        try:
            res = requests.get(self.update_url)
            res.raise_for_status()
            version_data = res.json()
            if version_data['name'] != version.__version__:
                return True, {
                    'version': version_data['name'],
                    'description': version_data['body'],
                    'download_link': version_data['zipball_url'],
                    'update_lib': False,
                }
            else:
                return False, {}
        except (ConnectionRefusedError, ConnectionError, HTTPError):
            _logger.error('cannot connect to base url to get updating information')
            raise

    @classmethod
    def _delete(cls, path):
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)

    @classmethod
    def _download_file(cls, download_link, file_name):
        res = requests.get(download_link, stream=True)
        res.raise_for_status()
        with open(os.path.join(utils.data_dir_path, file_name), mode='wb') as f:
            for chunk in res.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    @classmethod
    def _backup_file(cls, backup_path):
        if os.path.exists(backup_path):
            cls._delete(backup_path)
        os.mkdir(backup_path)

        excluded = set()
        for root, dirs, files in os.walk(utils.application_path):
            for f in files + dirs:
                if f in EXCLUDE_IN_BACKUP_RESTORE:
                    excluded.add(os.path.join(root, f))
                    continue
                src = os.path.join(root, f)
                if any(os.path.commonpath([src, exclude]) == exclude for exclude in excluded):
                    continue
                dst = os.path.join(backup_path, os.path.relpath(root, utils.application_path), f)
                dst_dir = os.path.dirname(dst)
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)
                os.rename(src, dst)

    @classmethod
    def _install_file(cls, file_zip):
        extract_dir = installer_dir = os.path.join(utils.data_dir_path, os.path.splitext(os.path.basename(file_zip))[0])
        if os.path.exists(extract_dir):
            for f in os.listdir(extract_dir):
                cls._delete(os.path.join(extract_dir, f))

        with zipfile.ZipFile(file_zip, 'r') as f:
            f.extractall(extract_dir)

        for d in os.listdir(extract_dir):
            installer_dir = os.path.join(extract_dir, d)
            break

        excluded = set()
        for root, dirs, files in os.walk(installer_dir):
            for f in files + dirs:
                if f in EXCLUDE_IN_BACKUP_RESTORE:
                    excluded.add(os.path.join(root, f))
                    continue
                src = os.path.join(root, f)
                if any(os.path.commonpath([src, exclude]) == exclude for exclude in excluded):
                    continue
                dst = os.path.join(utils.application_path, os.path.relpath(src, installer_dir))
                dst_dir = os.path.dirname(dst)
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)
                os.rename(src, dst)

        try:
            cls._delete(extract_dir)
        except Exception:
            pass

    @classmethod
    def _restore_file(cls, backup_path):
        for f in os.listdir(backup_path):
            os.rename(os.path.join(backup_path, f), os.path.join(utils.application_path, f))
        cls._delete(backup_path)

    def update(self, updating_data, callback):
        """
        :param updating_data: response from http request
        :param callback: callback function
        """
        # update to new version
        update_file = os.path.join(utils.data_dir_path, f'update_{updating_data["version"]}.zip')
        callback('Updating: 10%')

        if not os.path.exists(update_file):
            self._download_file(updating_data['download_link'], update_file)
            callback('Updating: 40%')
        callback('Updating: 60%')
        backup_path = os.path.join(utils.data_dir_path, f'backup_{version.__version__}')
        self._backup_file(backup_path)
        try:
            self._install_file(update_file)
        except Exception as e:
            self._restore_file(backup_path)
            raise e
        finally:
            self._delete(backup_path)
        callback('Updating: 80%')
        if updating_data.get('update_lib'):
            os.system(f'{utils.python_venv_exec_path} -m pip install -r "{utils.requirements_path}"')
        callback('Updating: 100%')
