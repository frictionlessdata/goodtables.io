from flask_oauthlib.client import OAuth
from flask_login import LoginManager, current_user

from goodtablesio import settings
from goodtablesio.services import database
from goodtablesio.models.user import User

GITHUB_OAUTH_SCOPES = ['user', 'repo', 'admin:repo_hook']


oauth = OAuth()

login_manager = LoginManager()


github_auth = oauth.remote_app(
    'github_auth',
    consumer_key=settings.GITHUB_CLIENT_ID,
    consumer_secret=settings.GITHUB_CLIENT_SECRET,
    request_token_params={'scope': ' '.join(GITHUB_OAUTH_SCOPES)},
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize'
)


@github_auth.tokengetter
def get_github_oauth_token():
    if current_user.is_authenticated:
        return current_user.github_oauth_token
    return None


@login_manager.user_loader
def load_user(user_id):
    return database['session'].query(User).filter_by(id=user_id).one_or_none()
