import pytest

from goodtablesio.models.user import User
from goodtablesio.tests import factories
from goodtablesio.services import database


pytestmark = pytest.mark.usefixtures('session_cleanup')


def test_create_user_stored_in_db():

    params = {
        'id': 'my-id',
        'name': 'my-name-2',
        'email': 'my-email-2@example.com',
        'admin': True,
        'display_name': 'Test User'
    }

    database['session'].add(User(**params))
    database['session'].commit()

    # Make sure that we are not checking the cached object in the session
    database['session'].remove()

    user = database['session'].query(User).get('my-id')

    assert user

    assert user.id == 'my-id'
    assert user.name == 'my-name-2'
    assert user.email == 'my-email-2@example.com'
    assert user.display_name == 'Test User'
    assert user.admin is True


def test_create_user_stored_in_db_no_email():

    params = {
        'id': 'my-id',
        'name': 'my-name-2',
        'email': None,
        'admin': True,
        'display_name': 'Test User'
    }

    database['session'].add(User(**params))
    database['session'].commit()

    # Make sure that we are not checking the cached object in the session
    database['session'].remove()

    user = database['session'].query(User).get('my-id')

    assert user

    assert user.id == 'my-id'
    assert user.name == 'my-name-2'
    assert user.email is None
    assert user.display_name == 'Test User'
    assert user.admin is True


def test_update_user_stored_in_db():

    params = {
        'id': 'my-id',
        'name': 'my-name-2',
        'email': 'my-email-2@example.com',
        'admin': True,
        'display_name': 'Test User'
    }

    database['session'].add(User(**params))
    database['session'].commit()

    # Make sure that we are not checking the cached object in the session
    database['session'].remove()

    user = database['session'].query(User).get('my-id')

    assert user

    user.email = 'a@a.com'
    database['session'].add(user)
    database['session'].commit()

    database['session'].remove()

    user = database['session'].query(User).get('my-id')

    assert user.email == 'a@a.com'
