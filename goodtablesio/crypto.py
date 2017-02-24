import binascii
from cryptography.fernet import Fernet

from goodtablesio import settings


def _get_crypto_instance(key):
    try:
        return Fernet(key)
    except binascii.Error:
        raise ValueError('Wrong secret key provided, it must be a 32 bit '
                         'URL-safe base64 string')


def encrypt_string(value, key=settings.GTIO_SECRET_KEY):

    f = _get_crypto_instance(key)

    # Ensure we are working with bytes
    if not hasattr(value, 'decode'):
        value = value.encode('utf-8')

    # Return a string
    return f.encrypt(value).decode('utf-8')


def decrypt_string(token, key=settings.GTIO_SECRET_KEY):

    f = _get_crypto_instance(key)

    # Ensure we are working with bytes
    if not hasattr(token, 'decode'):
        token = token.encode('utf-8')

    # Return a string
    return f.decrypt(token).decode('utf-8')
