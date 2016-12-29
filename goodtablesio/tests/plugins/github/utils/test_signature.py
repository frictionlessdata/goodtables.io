from goodtablesio.plugins.github.utils.signature import (
    create_signature, validate_signature)


# Tests

def test_create_signature():
    key = 'key'
    text = 'text'
    signature = 'sha1=369e2959eb49450338b212748f77d8ded74847bb'
    assert create_signature(key, text) == signature


def test_validate_signature():
    key = 'key'
    text = 'text'
    signature = 'sha1=369e2959eb49450338b212748f77d8ded74847bb'
    assert validate_signature(key, text, signature)


def test_validate_signature_invalid():
    key = 'key'
    text = 'text'
    signature = 'sha1=369e2959eb49450338b212748f77d8ded74-----'
    assert not validate_signature(key, text, signature)
