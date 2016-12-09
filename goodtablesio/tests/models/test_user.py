import pytest

from goodtablesio import models, services
from goodtablesio.tests import factories


pytestmark = pytest.mark.usefixtures('session_cleanup')


def test_create_user_outputs_dict():

    user = models.user.create({
        'id': 'my-id',
        'name': 'my-name',
        'email': 'my-email@example.com',
        'admin': True,

    })

    assert user['id'] == 'my-id'
    assert user['name'] == 'my-name'
    assert user['email'] == 'my-email@example.com'
    assert user['admin'] is True
    assert user['created']


def test_create_user_stored_in_db():

    params = {
        'id': 'my-id',
        'name': 'my-name-2',
        'email': 'my-email-2@example.com',
        'admin': True,
        'display_name': 'Test User'
    }

    models.user.create(params)

    # Make sure that we are not checking the cached object in the session
    services.db_session.remove()

    user = services.db_session.query(models.user.User).get('my-id')

    assert user

    assert user.id == 'my-id'
    assert user.name == 'my-name-2'
    assert user.email == 'my-email-2@example.com'
    assert user.display_name == 'Test User'
    assert user.admin is True


def test_update_user_outputs_dict():

    user = factories.User()

    params = {
        'id': user.id,
        'name': 'some-other-name',
        'email': 'updated@example.com',
    }

    updated_user = models.user.update(params)

    assert updated_user['id'] == user.id
    assert updated_user['name'] == 'some-other-name'
    assert updated_user['email'] == 'updated@example.com'


def test_update_user_stored_in_db():

    user = factories.User()

    params = {
        'id': user.id,
        'name': 'some-other-name',
        'email': 'updated@example.com',
    }

    models.user.update(params)

    # Make sure that we are not checking the cached object in the session
    services.db_session.remove()

    updated_user = services.db_session.query(models.user.User).get(user.id)

    assert updated_user

    assert updated_user.id == user.id
    assert updated_user.name == 'some-other-name'
    assert updated_user.email == 'updated@example.com'


def test_update_user_no_id_raises_value_error():
    with pytest.raises(ValueError):
        assert models.user.update({})


def test_update_user_not_found_raises_value_error():
    with pytest.raises(ValueError):
        assert models.user.update({'id': 'not-found'})


def test_get_user_outputs_dict():

    # Actually save it to the DB so we can test retrieving it
    user_db = factories.User(_save_in_db=True).to_dict()

    services.db_session.remove()

    user = models.user.get(user_db['id'])

    assert user['id'] == user_db['id']
    assert user['name'] == user_db['name']
    assert user['display_name'] == user_db['display_name']
    assert user['email'] == user_db['email']
    assert user['created'] == user_db['created']
    assert user['admin'] == user_db['admin']


def test_get_user_not_found_outputs_none():

    assert models.user.get('not-found') is None


def test_get_all():
    user1 = factories.User()
    user2 = factories.User()
    user3 = factories.User()

    all_users = models.user.get_all()

    assert len(all_users) == 3

    assert all_users == [user3.to_dict(), user2.to_dict(), user1.to_dict()]


def test_get_ids():
    user1 = factories.User()
    user2 = factories.User()

    assert models.user.get_ids() == [user2.id, user1.id]
