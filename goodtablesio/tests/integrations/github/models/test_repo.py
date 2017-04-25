import pytest
from goodtablesio.tests import factories
from goodtablesio.services import database
from goodtablesio.integrations.github.models.repo import GithubRepo
pytestmark = pytest.mark.usefixtures('session_cleanup')


# Tests

def test_create():
    repo = GithubRepo(id='id', name='owner/repo')
    database['session'].add(repo)
    database['session'].commit()
    repos = database['session'].query(GithubRepo).all()
    assert len(repos) == 1
    assert repos[0].id == 'id'
    assert repos[0].name == 'owner/repo'
    assert repos[0].owner == 'owner'
    assert repos[0].repo == 'repo'
    assert repos[0].active is False
    assert repos[0].url == 'https://github.com/owner/repo'


def test_update():
    repo = factories.GithubRepo()
    (database['session'].query(GithubRepo).
        filter_by(id=repo.id).
        update({'name': 'owner/new_repo'}))
    database['session'].commit()
    repos = database['session'].query(GithubRepo).all()
    assert len(repos) == 1
    assert repos[0].repo == 'new_repo'


def test_user_relationship():
    user = factories.User()
    repo = GithubRepo(id='id', name='owner/repo', users=[user])
    database['session'].add(repo)
    database['session'].commit()
    repos = database['session'].query(GithubRepo).all()
    assert len(repos) == 1
    assert repos[0].users[0].id == user.id


def test_new_source_job_number():

    source = GithubRepo()

    database['session'].add(source)
    database['session'].commit()

    assert source.job_number == 1
