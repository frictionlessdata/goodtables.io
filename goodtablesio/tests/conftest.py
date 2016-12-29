import pytest
from goodtablesio.app import app
from goodtablesio.services import database
from goodtablesio.models.job import Job
from goodtablesio.models.user import User
from goodtablesio.celery_app import celery_app as celapp
from goodtablesio.plugins.github.models.repo import GithubRepo


# Fixture

@pytest.fixture()
def session_cleanup():

    # TODO: rebase on cascade delete on some level (SA/DB)
    database['session'].execute('DELETE FROM users_github_repos')
    database['session'].query(Job).delete()
    database['session'].query(User).delete()
    database['session'].query(GithubRepo).delete()

    yield


@pytest.fixture()
def client():

    with app.test_client() as c:

        # Save a reference to the app for convenience
        c.app = app

        yield c


@pytest.fixture()
def celery_app():

    # We don't need to restore it because tests
    # always use eager (non forking) mode
    celapp.conf['task_always_eager'] = True

    return celapp
