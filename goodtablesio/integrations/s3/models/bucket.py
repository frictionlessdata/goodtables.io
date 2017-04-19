import cryptography

from goodtablesio.models.source import Source
from goodtablesio.crypto import encrypt_string, decrypt_string


class S3Bucket(Source):

    __mapper_args__ = {
        'polymorphic_identity': 's3'
    }

    @property
    def access_key_id(self):
        return self._get_encrypted('access_key_id')

    @access_key_id.setter
    def access_key_id(self, value):
        return self._set_encrypted('access_key_id', value)

    @access_key_id.deleter
    def access_key_id(self):
        del self.conf['access_key_id']

    @property
    def secret_access_key(self):
        return self._get_encrypted('secret_access_key')

    @secret_access_key.setter
    def secret_access_key(self, value):
        return self._set_encrypted('secret_access_key', value)

    @secret_access_key.deleter
    def secret_access_key(self):
        del self.conf['secret_access_key']

    # Private

    def _get_encrypted(self, key):
        token = self.conf.get(key)
        if token:
            try:
                token = decrypt_string(token)
            except cryptography.fernet.InvalidToken:
                # This happens if someone sets the key directly
                # on the conf property (ie it should never happen)
                token = None

        return token

    def _set_encrypted(self, key, value):
        if not self.conf:
            self.conf = {}
        self.conf[key] = encrypt_string(value)
