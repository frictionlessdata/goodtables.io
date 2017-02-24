import pytest
from goodtablesio.tests import factories
from goodtablesio.services import database
from goodtablesio.models.user import User

pytestmark = pytest.mark.usefixtures('session_cleanup')


def test_github_oauth_token_get():

    user = factories.User(github_oauth_token='xxx')

    assert user.github_oauth_token == 'xxx'


def test_github_oauth_token_get_unencrypted():

    user = factories.User(conf={'github_oauth_token': 'xxx'})

    assert user.github_oauth_token is None


def test_github_oauth_token_set():

    user = factories.User()

    user.github_oauth_token = 'xxx'

    # Encrypted
    assert user.conf['github_oauth_token'].startswith('gAAA')

    database['session'].commit()
    user_db = database['session'].query(User).first()

    assert user_db.github_oauth_token == 'xxx'


def test_github_oauth_token_del():

    user = factories.User(github_oauth_token='xxx')

    del user.github_oauth_token

    assert user.github_oauth_token is None

    database['session'].commit()
    user_db = database['session'].query(User).first()

    assert user_db.github_oauth_token is None
