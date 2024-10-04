import platform
from datetime import datetime, timezone

if platform.system() != 'Windows':
    raise Exception("This file is only used for Windows")

import clr
import base64
import os

from System.Security.Cryptography.X509Certificates import X509Certificate2, X509Store, StoreName, StoreLocation, OpenFlags, X509NameType, X509ContentType
from System.Security.Cryptography import HashAlgorithmName, RSASignaturePadding, CryptographicException
from System import Convert, DateTimeOffset

from pyhanko.sign import signers
from asn1crypto import x509


def get_signing_certs():
    # get signing cert from certificate store
    store = X509Store(StoreName.My, StoreLocation.CurrentUser)
    certificates = []
    store.Open(OpenFlags.ReadOnly)
    for cert in store.Certificates:
        if cert.HasPrivateKey and cert.GetNameInfo(X509NameType.SimpleName, False) != 'localhost':
            certificates.append(cert)
    store.Close()
    return certificates


def get_signing_cert(serial_number: str):
    certs = get_signing_certs()
    for cert in certs:
        if str(int(cert.SerialNumber, 16)) == serial_number:
            return cert


def get_signing_cert_data():
    certs = get_signing_certs()
    data = []
    for cert in certs:
        valid_from = datetime.fromtimestamp(DateTimeOffset(cert.NotBefore).ToUnixTimeSeconds())
        valid_to = datetime.fromtimestamp(DateTimeOffset(cert.NotAfter).ToUnixTimeSeconds())
        data.append({
            'name': cert.GetNameInfo(X509NameType.SimpleName, False),
            'serial_number': str(int(cert.SerialNumber, 16)),
            'subject_list': cert.Subject.split(', '),
            'valid_from': valid_from.isoformat(),
            'valid_to': valid_to.isoformat(),
            'is_expired': valid_to < datetime.now(),
        })
    return data


def convert_window_x509cert2_to_asn1x509cert(x509cert2: X509Certificate2) -> x509.Certificate:
    cert_data = x509cert2.Export(X509ContentType.Cert)
    certificate = x509.Certificate.load(bytes(cert_data))
    return certificate


def digital_sign(cert: X509Certificate2, to_sign: bytes) -> bytes:
    rsa = cert.get_PrivateKey()
    try:
        signature = rsa.SignData(to_sign, HashAlgorithmName.SHA256, RSASignaturePadding.Pkcs1)
    except CryptographicException as e:
        if 'Invalid algorithm specified' in str(e):
            signature = rsa.SignData(to_sign, HashAlgorithmName.SHA1, RSASignaturePadding.Pkcs1)
        else:
            raise
    return bytes(signature)


class WindowCertStoreSigner(signers.ExternalSigner):
    async def async_sign_raw(
        self, data: bytes, digest_algorithm: str, dry_run=False
    ) -> bytes:
        if dry_run:
            return b'0' * 512
        windows_cert = get_signing_cert(str(self.signing_cert.serial_number))
        return digital_sign(windows_cert, data)
