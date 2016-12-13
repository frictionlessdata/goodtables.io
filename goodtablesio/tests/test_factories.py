import pytest

from goodtablesio import services
from goodtablesio.models.job import Job
from goodtablesio.models.user import User
from goodtablesio.tests import factories

pytestmark = pytest.mark.usefixtures('session_cleanup')


def test_create_job():
    job = factories.Job()

    assert job.status == 'created'
    assert job.plugin_name == 'api'

    job_db = services.db_session.query(Job).get(job.id)

    assert job_db.id == job.id


def test_build_job():
    job = factories.Job.build()

    job_db = services.db_session.query(Job).get(job.id)

    assert job_db is None


def test_create_job_are_different():

    job1 = factories.Job()
    job2 = factories.Job()

    assert job1.id != job2.id

    assert job1.created != job2.created


def test_create_job_overrides():
    job = factories.Job(id='my-id', report={'a': 'b'})

    assert job.id == 'my-id'
    assert job.report == {'a': 'b'}


def test_create_user():
    user = factories.User()

    assert user.name
    assert user.display_name
    assert user.email
    assert user.admin is False

    user_db = services.db_session.query(User).get(user.id)

    assert user_db.id == user.id


def test_create_user_are_different():

    user1 = factories.User()
    user2 = factories.User()
    assert user1.id != user2.id

    assert user1.created != user2.created


def test_create_user_overrides():
    user = factories.User(id='my-id', name='my-name', admin=True,
                          provider_ids={'github': '123'})

    assert user.id == 'my-id'
    assert user.name == 'my-name'
    assert user.admin is True
    assert user.provider_ids['github'] == '123'
