import asyncio
import base64
import random
import string
import tempfile
from io import BytesIO

import requests
import os
import logging

_logger = logging.getLogger(__name__)

from PIL import Image
from pyhanko import stamp
from pyhanko.pdf_utils import images

from pyhanko.sign import signers, timestamps
from pyhanko.sign.general import SigningError
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.sign.fields import SigFieldSpec

from .server_service import app, websocket_handler, WebsocketHandler
from .. import pkcs11_utils

def random_str(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@websocket_handler
class WebsocketHandlerV1(WebsocketHandler):
    api_version = 'v1'

    async def process(self, data):
        if data['action'] == 'get_windows_certs':
           await self._get_windows_certs(data)
        elif data['action'] == 'sign':
            cert_data = data['cert_data']
            if cert_data['type'] == 'windows_cert':
                await self._windows_cert_sign(data)
            elif cert_data['type'] == 'pkcs11_cert':
                await self._pkcs11_path_sign(data)
            else:
                await self.manager.send_error(f'unknown type: {cert_data["type"]}', self.websocket)
        elif data['action'] == 'pkcs11_path_get_all_certs_and_token_info':
            await self._pkcs11_path_get_all_certs_and_token_info(data)

    async def _windows_cert_sign(self, data):
        if os.name != 'nt':
            await self.manager.send_error(f'Os name does not match (Windows)', self.websocket)
            return

        cert_data = data['cert_data']
        from app import windows_signer
        cert = windows_signer.get_signing_cert(cert_data["serial_number"])
        if not cert:
            await self.manager.send_error(f'Cert {cert_data["serial_number"]} not found!', self.websocket)
            return
        singer = windows_signer.WindowCertStoreSigner(
            signing_cert=windows_signer.convert_window_x509cert2_to_asn1x509cert(cert),
            cert_registry=None
        )
        await self._try_sign(data, singer)

    async def _pkcs11_path_sign(self, data):
        cert_data = data['cert_data']
        signing_cert = await pkcs11_utils.find_cert(cert_data['pkcs11_path'], cert_data['serial_number'])
        pkcs11_signer = pkcs11_utils.Pkcs11Signer(
            pkcs11_path=cert_data['pkcs11_path'],
            password=cert_data['pin_code'],
            signing_cert=signing_cert
        )
        await self._try_sign(data, pkcs11_signer)

    async def _try_sign(self, data, signer: signers.Signer, current_call=1, max_try=2):
        try:
            await self._sign(data, signer)
        except SigningError as e:
            if current_call > max_try:
                raise
            if 'Signature field with name appears to be filled already' in str(e):
                data['signature_field_name'] = None
                await self._try_sign(data, signer, current_call=current_call+1)

    async def _sign(self, data, singer: signers.Signer):
        response = requests.get(data['file_url'], verify=False, stream=True)
        if response.status_code != 200:
            await self.manager.send_error(f'download {data["file_url"]} error', self.websocket)
            return

        signature_field_name = data['signature_field_name'] or f'Signature_{random_str(12)}'
        with tempfile.TemporaryFile() as temp_file:
            for chunk in response.iter_content(chunk_size=8069):
                temp_file.write(chunk)

            writer = IncrementalPdfFileWriter(temp_file, strict=False)
            signature_image_base64 = base64.b64decode(data['signature_image'])
            signature_image = Image.open(BytesIO(signature_image_base64))
            signature_coords = data['signature_coords']

            box = (
                signature_coords['x1'],
                signature_coords['y1'],
                signature_coords['x2'],
                signature_coords['y2']
            )
            if os.name == 'nt':
                box = (
                    signature_coords['x1'],
                    signature_coords['y2'],
                    signature_coords['x2'],
                    signature_coords['y1']
                )
            border_width = 0.5 if data.get('has_border') else 0

            timestamper = None
            if data.get('timestamp_server'):
                timestamper = timestamps.HTTPTimeStamper(data['timestamp_server'])
            pdf_signer = signers.PdfSigner(
                signature_meta=signers.PdfSignatureMetadata(
                    field_name=signature_field_name
                ),
                new_field_spec=SigFieldSpec(
                    sig_field_name=signature_field_name,
                    on_page=data['on_page'] - 1,
                    box=box
                ),
                stamp_style=stamp.TextStampStyle(
                    stamp_text='',
                    background=images.PdfImage(signature_image),
                    background_opacity=1,
                    border_width=border_width
                ),
                signer=singer,
                timestamper=timestamper
            )
            try:
                output = await pdf_signer.async_sign_pdf(writer)
            except Exception as e:
                await self.manager.send_error(str(e), self.websocket)
                raise
            await self.manager.send_personal_json({
                'action': 'sign_done',
                'signature_field_name': signature_field_name,
                'pdf_data': base64.b64encode(output.getvalue()).decode('utf-8')
            }, self.websocket)

    async def _get_windows_certs(self, data):
        if os.name == 'nt':
            from app import windows_signer
            data = {
                'type': 'windows_cert',
                'action': 'get_windows_certs',
                'certs': windows_signer.get_signing_cert_data()
            }
            await self.manager.send_personal_json(data, self.websocket)
        else:
            await self.manager.send_error('Get Windows certificates in your os is not supported', self.websocket)

    async def _pkcs11_path_get_all_certs_and_token_info(self, data):
        if not os.path.exists(data['path']):
            await self.manager.send_error(
                f'Path {data["path"]} does not exist on your local machine',
                self.websocket
            )
        try:
            get_certs_task = pkcs11_utils.pkcs11_get_all_certificates(data['path'])
            get_token_info_task = pkcs11_utils.pkcs11_get_token_info(data['path'])
            certs_data, token_info = await asyncio.gather(get_certs_task, get_token_info_task)
            _certs = [{
                'name': data['name'],
                'serial_number': data['serial_number'],
                'subject_list': data['subject_list'],
                'valid_from': data['valid_from'],
                'valid_to': data['valid_to'],
                'is_expired': data['is_expired']
            } for data in certs_data]
            result = {
                'action': 'pkcs11_path_get_all_certs_and_token_info',
                'path': data['path'],
                'certs': _certs,
                'token_info': token_info
            }
            await self.manager.send_personal_json(result, self.websocket)
        except Exception as e:
            await self.manager.send_error(f'Error: {e}', self.websocket)
            raise
