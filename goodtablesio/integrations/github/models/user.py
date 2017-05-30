import cryptography
from goodtablesio.crypto import encrypt_string, decrypt_string
from goodtablesio.models.user import User


# Helpers

def get_token(self):
    token = self.conf.get('github_oauth_token')
    if token:
        try:
            token = decrypt_string(token)
        except cryptography.fernet.InvalidToken:
            # This happens if someone sets the github_oauth_token directly
            # on the conf property (ie it should never happen)
            token = None

    return token


def set_token(self, value):
    if not self.conf:
        self.conf = {}
    self.conf['github_oauth_token'] = encrypt_string(value)


def del_token(self):
    del self.conf['github_oauth_token']


# Module API

setattr(User, 'github_oauth_token', property(
    get_token, set_token, del_token, 'GitHub OAuth Token'))
