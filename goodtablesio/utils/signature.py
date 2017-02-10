import hmac
import hashlib


# Module API

def create_signature(key, text):
    """Create signature for text.
    """
    if isinstance(key, str):
        key = key.encode('utf-8')
    if isinstance(text, str):
        text = text.encode('utf-8')
    mac = hmac.new(key, msg=text, digestmod=hashlib.sha1)
    return 'sha1=%s' % mac.hexdigest()


def validate_signature(key, text, signature):
    """Validate text against signature.
    """
    return hmac.compare_digest(create_signature(key, text), signature)
