import pytest

from goodtablesio.services import database
from goodtablesio.models.plan import Plan
from goodtablesio.integrations.github.tasks.repos import sync_user_repos
from goodtablesio.tests import factories

pytestmark = pytest.mark.usefixtures('session_cleanup')


# Tests

def test_sync_user_repos(celery_app, GitHubForIterRepos):
    job = factories.InternalJob()
    user = factories.User(github_oauth_token='my-token')
    sync_user_repos(user.id, job_id=job.id)
    GitHubForIterRepos.assert_called_with(token='my-token')
    sources = sorted(user.sources, key=lambda source: source.name)

    assert len(sources) == 2

    assert sources[0].conf['github_id'] == 'id1'
    assert sources[0].name == 'owner1/repo1'
    assert sources[0].active is True
    assert sources[0].conf['private'] is False
    assert sources[1].conf['github_id'] == 'id2'
    assert sources[1].name == 'owner2/repo2'
    assert sources[1].active is False
    assert sources[1].conf['private'] is False

    assert sorted(user.conf['github_orgs']) == ['owner1', 'owner2']


def test_sync_user_admin_can_see_private(celery_app, GitHubForIterRepos):
    job = factories.InternalJob()
    user = factories.User(admin=True, github_oauth_token='my-token')
    sync_user_repos(user.id, job_id=job.id)
    GitHubForIterRepos.assert_called_with(token='my-token')
    sources = sorted(user.sources, key=lambda source: source.name)

    assert len(sources) == 3

    assert sources[0].conf['github_id'] == 'id1'
    assert sources[0].conf['private'] is False
    assert sources[1].conf['github_id'] == 'id2'
    assert sources[1].conf['private'] is False
    assert sources[2].conf['github_id'] == 'id3'
    assert sources[2].conf['private'] is True


def test_sync_user_with_plan_can_see_private(celery_app, GitHubForIterRepos):
    job = factories.InternalJob()

    plan = database['session'].query(Plan).filter_by(name='paid').one()

    user = factories.User(admin=True, github_oauth_token='my-token')
    user.set_plan(plan.name)

    sync_user_repos(user.id, job_id=job.id)
    GitHubForIterRepos.assert_called_with(token='my-token')
    sources = sorted(user.sources, key=lambda source: source.name)

    assert len(sources) == 3

    assert sources[0].conf['github_id'] == 'id1'
    assert sources[0].conf['private'] is False
    assert sources[1].conf['github_id'] == 'id2'
    assert sources[1].conf['private'] is False
    assert sources[2].conf['github_id'] == 'id3'
    assert sources[2].conf['private'] is True
