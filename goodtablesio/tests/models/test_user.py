import datetime

import pytest

from goodtablesio.models.user import User
from goodtablesio.models.plan import Plan
from goodtablesio.models.subscription import Subscription
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


def test_json_fields_mutable():

    user = factories.User(id='my-id', provider_ids={'github': 123456},
                          conf={'a': '1'}, _save_in_db=True)

    user.provider_ids.update({'google': 'abcd'})
    user.conf.update({'b': '2'})

    database['session'].add(user)
    database['session'].commit()

    database['session'].remove()

    user = database['session'].query(User).get('my-id')

    assert user.provider_ids == {'google': 'abcd', 'github': 123456}
    assert user.conf == {'a': '1', 'b': '2'}


def test_user_set_plan():

    plan = database['session'].query(Plan).filter_by(name='paid').one()

    user = factories.User()

    assert user.plan is None

    user.set_plan(plan.name)

    assert user.plan == plan

    subscriptions = database['session'].query(Subscription).filter_by(
        user_id=user.id).all()

    assert len(subscriptions) == 1

    assert subscriptions[0].user_id == user.id
    assert subscriptions[0].plan_id == plan.id
    assert subscriptions[0].active is True

    assert user.subscription.id == subscriptions[0].id


def test_user_set_plan_unknown():

    user = factories.User()
    with pytest.raises(ValueError):
        user.set_plan('not-found')


def test_user_set_plan_no_expire():

    plan = database['session'].query(Plan).filter_by(name='free').one()
    assert plan.frequency == ''

    user = factories.User()
    user.set_plan(plan.name)

    assert user.subscription.expires is None


def test_user_set_plan_expire_in_a_month():

    plan = database['session'].query(Plan).filter_by(name='paid').one()
    assert plan.frequency == 'month'

    user = factories.User()
    user.set_plan(plan.name)

    assert (user.subscription.expires.date() ==
            datetime.datetime.now().date() + datetime.timedelta(days=30))


def test_user_set_plan_expire_in_a_year():

    plan = factories.Plan(name='my-plan', frequency='year')

    user = factories.User()
    user.set_plan(plan.name)

    assert (user.subscription.expires.date() ==
            datetime.datetime.now().date() + datetime.timedelta(days=365))

    database['session'].delete(user.subscription)
    database['session'].delete(plan)
    database['session'].commit()


def test_user_set_plan_extend_subscription():

    plan = database['session'].query(Plan).filter_by(name='paid').one()
    assert plan.frequency == 'month'

    user = factories.User()
    user.set_plan(plan.name)

    user.extend_subscription()

    # Initial month + an extra one
    assert (user.subscription.expires.date() ==
            datetime.datetime.now().date() + datetime.timedelta(days=60))


def test_user_set_plan_extend_subscription_no_active_subscription():

    user = factories.User()
    with pytest.raises(ValueError):
        user.extend_subscription()


def test_create_api_token():
    user = factories.User()
    user.create_api_token()
    assert len(user.api_tokens) == 1
    assert len(user.api_tokens[0].token) == 40


def test_create_api_token_with_description():
    user = factories.User()
    user.create_api_token('description')
    assert len(user.api_tokens) == 1
    assert len(user.api_tokens[0].token) == 40
    assert user.api_tokens[0].description == 'description'


def test_delete_api_token():
    user = factories.User()
    token = user.create_api_token()
    assert user.delete_api_token(token.id) is True
    assert len(user.api_tokens) == 0


def test_delete_api_token_not_existent():
    user = factories.User()
    assert user.delete_api_token('not-existent') is False
    assert len(user.api_tokens) == 0


def test_get_by_api_token():
    user = factories.User()
    token = user.create_api_token()
    user = User.get_by_api_token(token.token)
    assert len(user.api_tokens) == 1
    assert len(user.api_tokens[0].token) == 40


def test_get_by_api_token_not_existent():
    user = User.get_by_api_token('not-existent')
    assert user is None
