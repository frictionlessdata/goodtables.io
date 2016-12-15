from flask import session
from flask_oauthlib.client import OAuth

from goodtablesio import config

GITHUB_OAUTH_SCOPES = ['user', 'repo', 'admin:repo_hook']


oauth = OAuth()


github_auth = oauth.remote_app(
    'github_auth',
    consumer_key=config.GITHUB_CLIENT_ID,
    consumer_secret=config.GITHUB_CLIENT_SECRET,
    request_token_params={'scope': ' '.join(GITHUB_OAUTH_SCOPES)},
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize'
)


@github_auth.tokengetter
def get_github_oauth_token():
    return session.get('github_token')
