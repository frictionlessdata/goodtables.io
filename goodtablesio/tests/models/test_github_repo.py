import pytest
from goodtablesio.tests import factories
from goodtablesio.services import database
from goodtablesio.models.github_repo import GithubRepo
pytestmark = pytest.mark.usefixtures('session_cleanup')
session = database['session']


# Tests

def test_create():
    repo = GithubRepo(id='id', owner='owner', repo='repo')
    session.add(repo)
    session.commit()
    repos = session.query(GithubRepo).all()
    assert len(repos) == 1
    assert repos[0].id == 'id'
    assert repos[0].owner == 'owner'
    assert repos[0].repo == 'repo'
    assert repos[0].active is False
    assert repos[0].url == 'https://github.com/owner/repo'


def test_update():
    repo = factories.GithubRepo()
    session.query(GithubRepo).filter_by(id=repo.id).update({'repo': 'new_repo'})
    session.commit()
    repos = session.query(GithubRepo).all()
    assert len(repos) == 1
    assert repos[0].repo == 'new_repo'


def test_user_relationship():
    user = factories.User()
    repo = GithubRepo(id='id', owner='owner', repo='repo', users=[user])
    session.add(repo)
    session.commit()
    repos = session.query(GithubRepo).all()
    assert len(repos) == 1
    assert repos[0].users[0].id == user.id
