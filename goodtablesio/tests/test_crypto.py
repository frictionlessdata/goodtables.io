import pytest
from cryptography.fernet import Fernet

from goodtablesio import settings
from goodtablesio.crypto import encrypt_string, decrypt_string


def test_incorrect_key_encrypt():

    value = b'some-text'
    key = b'incorrect-key'

    with pytest.raises(ValueError) as exc:
        encrypt_string(value, key=key)

        assert 'Wrong secret key' in str(exc)


def test_encrypt_string():

    value = b'some-text'
    key = Fernet.generate_key()
    f = Fernet(key)

    token = encrypt_string(value, key=key)

    assert isinstance(token, str)

    assert f.decrypt(token.encode('utf-8')) == value


def test_encrypt_string_uses_key_in_settings_by_default():

    value = b'some-text'
    key = settings.GTIO_SECRET_KEY
    f = Fernet(key)

    token = encrypt_string(value)

    assert f.decrypt(token.encode('utf-8')) == value


def test_encrypt_string_transforms_to_bytes():

    value = 'some-text'
    key = Fernet.generate_key()
    f = Fernet(key)

    token = encrypt_string(value, key=key)

    assert f.decrypt(token.encode('utf-8')) == value.encode('utf-8')


def test_incorrect_key_decrypt():

    token = b'some-token'
    key = b'incorrect-key'

    with pytest.raises(ValueError) as exc:
        decrypt_string(token, key=key)

        assert 'Wrong secret key' in str(exc)


def test_decrypt_string():

    value = b'some-text'
    key = Fernet.generate_key()
    f = Fernet(key)
    token = f.encrypt(value)

    our_value = decrypt_string(token, key=key)

    assert isinstance(our_value, str)

    assert our_value == value.decode('utf-8')


def test_decrypt_string_uses_key_in_settings_by_default():

    value = b'some-text'
    key = settings.GTIO_SECRET_KEY
    f = Fernet(key)
    token = f.encrypt(value)

    our_value = decrypt_string(token)

    assert our_value == value.decode('utf-8')


def test_decrypt_string_transforms_to_bytes():

    value = b'some-text'
    key = settings.GTIO_SECRET_KEY
    f = Fernet(key)
    token = f.encrypt(value)

    our_value = decrypt_string(token.decode('utf-8'))

    assert our_value == value.decode('utf-8')
