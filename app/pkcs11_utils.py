import PyKCS11
from PyKCS11 import _LowLevel

from datetime import datetime, timezone, timedelta
from typing import Optional, Union

from asn1crypto import x509
from pyhanko.sign import signers


from asn1crypto.algos import SignedDigestAlgorithm

certs_data_cache = {}


async def pkcs11_get_all_certificates(path, slot=0, only_certs=False, cache=True):
    global certs_data_cache
    now = datetime.now()
    hash_value = hash(f'{path}{slot}')
    if cache and hash_value in certs_data_cache:
        cache_value = certs_data_cache[hash_value]
        if cache_value['cache_time'] > now:
            if only_certs:
                return [data['cert'] for data in cache_value['cert_data']]
            return cache_value['cert_data']

    pkcs11 = PyKCS11.PyKCS11Lib()
    pkcs11.load(path)
    slots = pkcs11.getSlotList(tokenPresent=True)
    if not slots:
        raise Exception("Token is not inserted")
    session = pkcs11.openSession(slots[slot])
    certificate_objects = session.findObjects([(_LowLevel.CKA_CLASS, _LowLevel.CKO_CERTIFICATE)])

    certs_data = []
    for cert_obj in certificate_objects:
        cert_attributes = session.getAttributeValue(cert_obj, [_LowLevel.CKA_VALUE])
        cert_der = bytes(cert_attributes[0])
        cert = x509.Certificate.load(cert_der)
        certs_data.append({
            'cert': cert,
            'name': cert.subject.native.get('common_name', ''),
            'serial_number': str(cert.serial_number),
            'subject_list': [f"{k}={v}" for k, v in cert.subject.native.items()],
            'valid_from': cert.not_valid_before.isoformat(),
            'valid_to': cert.not_valid_after.isoformat(),
            'is_expired': cert.not_valid_after < datetime.now(tz=timezone.utc),
        })
    certs_data_cache[hash_value] = {
        'cert_data': certs_data,
        'cache_time': datetime.now() + timedelta(hours=1),
    }
    session.closeSession()
    if only_certs:
        return [data['cert'] for data in certs_data]
    return certs_data


async def pkcs11_get_token_info(path, slot=0):
    pkcs11 = PyKCS11.PyKCS11Lib()
    pkcs11.load(path)
    slots = pkcs11.getSlotList(tokenPresent=True)
    token_info = pkcs11.getTokenInfo(slots[slot])
    return {
        'label': token_info.label.strip(),
        'model': token_info.model,
        'serial_number': token_info.serialNumber,
        'CKF_LOGIN_REQUIRED': token_info.flags & _LowLevel.CKF_LOGIN_REQUIRED,
        'CKF_USER_PIN_FINAL_TRY': token_info.flags & _LowLevel.CKF_USER_PIN_FINAL_TRY,
        'CKF_USER_PIN_LOCKED': token_info.flags & _LowLevel.CKF_USER_PIN_LOCKED,
    }


async def find_cert(path: str, serial_number: str, slot=0):
    all_certs = await pkcs11_get_all_certificates(path, slot=slot)
    for cert_data in all_certs:
        if cert_data['serial_number'] == serial_number:
            return cert_data['cert']


class Pkcs11Signer(signers.ExternalSigner):
    """
        Pyhanko has Pkcs11 support, but it has many bugs from another library, so we implement our own
    """
    def __init__(
        self,
        pkcs11_path: str,
        password: str,
        signing_cert: Optional[x509.Certificate]=None,
        signature_value: Union[bytes, int, None] = None,
        signature_mechanism: Optional[SignedDigestAlgorithm] = None,
        prefer_pss: bool = False,
        embed_roots: bool = True,
        slot=0,
    ):
        super().__init__(signing_cert, None, signature_value, signature_mechanism, prefer_pss, embed_roots)
        self.password = password
        self.slot = slot
        self.pkcs11_path = pkcs11_path

    async def async_sign_raw(
        self, data: bytes, digest_algorithm: str, dry_run=False
    ) -> bytes:
        if dry_run:
            return b'0' * 512
        pkcs11 = PyKCS11.PyKCS11Lib()
        pkcs11.load(self.pkcs11_path)

        session = None
        signature = None
        try:
            slot = pkcs11.getSlotList(tokenPresent=True)[self.slot]
            session = pkcs11.openSession(slot, _LowLevel.CKF_SERIAL_SESSION | _LowLevel.CKF_RW_SESSION)
            token_info = pkcs11.getTokenInfo(slot)
            if token_info.flags & _LowLevel.CKF_LOGIN_REQUIRED:
                session.login(self.password)

            mechanism = PyKCS11.Mechanism(_LowLevel.CKM_SHA256_RSA_PKCS, None)
            private_keys = session.findObjects([(_LowLevel.CKA_CLASS, _LowLevel.CKO_PRIVATE_KEY)])
            private_key = None

            certs = await pkcs11_get_all_certificates(self.pkcs11_path, self.slot, only_certs=True)
            for key in private_keys:
                if private_key:
                    break

                for cert in certs:
                    if cert.serial_number == self.signing_cert.serial_number:
                        private_key = key
                        break
            signature = session.sign(private_key, data, mechanism)
        finally:
            if session:
                try:
                    session.logout()
                except PyKCS11.PyKCS11Error as e:
                    if 'CKR_USER_NOT_LOGGED_IN' in str(e):
                        pass
                    else:
                        raise
                session.closeSession()
        return bytes(signature)
