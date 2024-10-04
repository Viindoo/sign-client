import os
import zipfile

import requests
import logging
from requests.exceptions import ConnectionError, HTTPError

import version
from app import utils

_logger = logging.getLogger(__name__)
base_update_url = 'https://viindoo.com'

class Updater:
    def __init__(self, data=None):
        data = data or {}
        self.base_url = data.get('base_url', base_update_url)

    def get_updating_data(self):
        try:
            res = requests.get(self.base_url + '/viin_sign_desktop/latest_version_data')
            res.raise_for_status()
            version_data = res.json()
            if version_data['version'] != version.__version__:
                return True, {
                    'version': version_data['version'],
                    'description': version_data['description'],
                    'download_link': version_data['download_link'],
                    'update_lib': version_data['update_lib'],
                }
            else:
                return False, {}
        except (ConnectionRefusedError, ConnectionError, HTTPError):
            _logger.error('cannot connect to base url to get updating information')
            raise

    @classmethod
    def _download_file(cls, download_link, file_name):
        res = requests.get(download_link, stream=True, verify=False)
        res.raise_for_status()
        with open(os.path.join(utils.data_dir_path, file_name)) as f:
            for chunk in res.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    @classmethod
    def _unzip_file(cls, file_zip, unzip_to):
        with zipfile.ZipFile(file_zip, 'r') as f:
            members = f.namelist()
            for zipinfo in members:
                try:
                    f._extract_member(zipinfo, unzip_to, os.getcwd())
                except PermissionError as e:
                    _logger.error(f'unzip file error {str(e)}')

    def update(self, updating_data, callback):
        """
        :param updating_data: response from http request
        :param callback: callback function
        """
        # update to new version
        update_file = os.path.join(utils.data_dir_path, f'update_{updating_data["version"]}.zip')
        callback('Updating: 10%')

        if os.path.exists(update_file):
           self._unzip_file(update_file, utils.application_path)
        else:
            self._download_file(updating_data['download_link'], update_file)
            callback('Updating: 40%')
            self._unzip_file(update_file, utils.application_path)
            callback('Updating: 80%')
        if updating_data.get('update_lib'):
            os.system(f'{utils.python_venv_exec_path} -m pip install -r "{utils.requirements_path}"')
        callback('Updating: 100%')
