from goodtablesio.models.user import User


def get_token(self):
    return self.conf.get('github_oauth_token')


def set_token(self, value):
    if not self.conf:
        self.conf = {}
    self.conf['github_oauth_token'] = value


def del_token(self):
    del self.conf['github_oauth_token']


github_oauth_token = property(
    get_token, set_token, del_token, 'GitHub OAuth Token')

setattr(User, 'github_oauth_token', github_oauth_token)
