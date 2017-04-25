import urllib
from unittest import mock

from flask import url_for, session
import pytest

from goodtablesio import settings, auth
from goodtablesio.tests import factories
from goodtablesio.services import database
from goodtablesio.models.user import User


# Clean up DB on all this module's tests

pytestmark = pytest.mark.usefixtures('session_cleanup')


def test_github_login_basic(client):

    with client.app.test_request_context():
        login_url = url_for('user.login', provider='github')
        authorized_url = url_for('user.authorized', provider='github',
                                 _external=True)

    response = client.get(login_url)

    assert response.status_code == 302
    assert response.headers['Location']
    parts = urllib.parse.urlparse(response.headers['Location'])

    assert parts.scheme == 'https'
    assert parts.netloc == 'github.com'
    assert parts.path == '/login/oauth/authorize'
    params = urllib.parse.parse_qs(parts.query)

    assert params['client_id'][0] == settings.GITHUB_CLIENT_ID
    assert params['redirect_uri'][0] == authorized_url
    assert params['scope'][0] == ' '.join(auth.GITHUB_OAUTH_SCOPES)


def test_github_login_already_logged_in(client):

    user = factories.User()

    with client.app.test_request_context():
        login_url = url_for('user.login', provider='github')
        home_url = url_for('site.home', _external=True)

    with client.session_transaction() as sess:
        # Mock a user login
        sess['user_id'] = user.id

    response = client.get(login_url)

    assert response.status_code == 302
    assert response.headers['Location'] == home_url


def test_logout(client):

    user = factories.User()

    with client.app.test_request_context():
        logout_url = url_for('user.logout')
        home_url = url_for('site.home', _external=True)

    with client.session_transaction() as sess:
        # Mock a user login
        sess['user_id'] = user.id

    response = client.get(logout_url)

    assert response.status_code == 302
    assert response.headers['Location'] == home_url

    assert 'user_id' not in session


@pytest.mark.usefixtures('session_cleanup')
def test_github_authorized_sets_session_and_redirects(
     client, mock_github_auth_response, mock_github_user_response):

    with client.app.test_request_context():
        authorized_url = url_for('user.authorized', provider='github')
        home_url = url_for('site.home', _external=True)

        assert 'user_id' not in session

    response = client.get(authorized_url)

    assert response.status_code == 302
    assert response.headers['Location'] == home_url

    assert 'user_id' in session


def test_github_authorized_wrong_oauth_response(
     client, mock_github_auth_response):

    mock_github_auth_response.reset_mock()
    mock_github_auth_response.return_value = {'sorry': 'no-token'}

    with client.app.test_request_context():
        authorized_url = url_for('user.authorized', provider='github')

    params = {'error': 'some-error', 'error_description': 'Some Error'}
    response = client.get(authorized_url, query_string=params)

    assert response.status_code == 401
    assert 'problem logging in' in response.get_data(as_text=True)


def test_github_authorized_no_user_details(
     client, mock_github_auth_response, mock_github_user_response):

    mock_github_user_response.reset_mock()
    mock_github_user_response.return_value = mock.Mock(status=401)

    with client.app.test_request_context():
        authorized_url = url_for('user.authorized', provider='github')

    response = client.get(authorized_url)

    assert response.status_code == 401
    assert 'could not get user details' in response.get_data(as_text=True)


def test_github_login_creates_new_user(
     client, mock_github_auth_response, mock_github_user_response):

    with client.app.test_request_context():
        authorized_url = url_for('user.authorized', provider='github')

    assert database['session'].query(User).all() == []

    client.get(authorized_url)

    users = database['session'].query(User).all()

    assert len(users) == 1

    assert users[0].name == 'test-user-from-github'
    assert users[0].display_name == 'Test User from GitHub'
    assert users[0].email == 'test-from-github@example.com'
    assert users[0].provider_ids == {'github': 123456}


def test_github_login_existing_user(
     client, mock_github_auth_response, mock_github_user_response):

    with client.app.test_request_context():
        authorized_url = url_for('user.authorized', provider='github')

    factories.User(provider_ids={'github': 123456})

    client.get(authorized_url)

    users = database['session'].query(User).all()

    assert len(users) == 1

    assert users[0].provider_ids == {'github': 123456}


def test_github_login_existing_user_same_email_different_provider(
     client, mock_github_auth_response, mock_github_user_response):

    with client.app.test_request_context():
        authorized_url = url_for('user.authorized', provider='github')

    factories.User(email='test-from-github@example.com',
                   provider_ids={'google': 'abcd'})

    client.get(authorized_url)

    users = database['session'].query(User).all()

    assert len(users) == 1

    assert users[0].email == 'test-from-github@example.com'
    assert users[0].provider_ids == {'google': 'abcd', 'github': 123456}


def test_github_login_existing_user_without_email(
     client, mock_github_auth_response, mock_github_user_response_no_email):

    with client.app.test_request_context():
        authorized_url = url_for('user.authorized', provider='github')

    factories.User(provider_ids={'github': 'xxx'}, email=None)

    client.get(authorized_url)

    users = database['session'].query(User).order_by(User.created.desc()).all()

    assert len(users) == 2

    assert users[0].provider_ids == {'github': 7891011}


def test_home(client):

    user = factories.User()

    with client.app.test_request_context():
        home_url = url_for('user.home')

    with client.session_transaction() as sess:
        # Mock a user login
        sess['user_id'] = user.id

    response = client.get(home_url)

    assert response.status_code == 200

    # TODO: update when proper content
    assert user.display_name in response.get_data(as_text=True)


def test_home_not_authorized(client):

    with client.app.test_request_context():
        home_url = url_for('user.home')

    response = client.get(home_url)

    assert response.status_code == 401


@pytest.fixture
def mock_github_auth_response():
    func = 'goodtablesio.auth.github_auth.authorized_response'
    with mock.patch(func) as mock_response:
        oauth_response = {
            'access_token': 'some-testing-token',
            'scope': ','.join(auth.GITHUB_OAUTH_SCOPES),
            'token_type': 'bearer'
        }

        mock_response.return_value = oauth_response
        yield mock_response
        mock.patch.stopall()


@pytest.fixture
def mock_github_user_response():
    with mock.patch('goodtablesio.auth.github_auth.get') as mock_get:
        user_response = mock.Mock()
        user_response.status = 200
        user_response.data = {
            'id': 123456,
            'login': 'test-user-from-github',
            'name': 'Test User from GitHub',
            'email': 'test-from-github@example.com'
        }

        mock_get.return_value = user_response
        yield mock_get
        mock.patch.stopall()


@pytest.fixture
def mock_github_user_response_no_email():
    with mock.patch('goodtablesio.auth.github_auth.get') as mock_get:
        user_response = mock.Mock()
        user_response.status = 200
        user_response.data = {
            'id': 7891011,
            'login': 'test-user-from-github',
            'name': 'Test User from GitHub',
            'email': None
        }

        mock_get.return_value = user_response
        yield mock_get
        mock.patch.stopall()
