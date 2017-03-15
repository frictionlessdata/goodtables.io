import pytest
from goodtablesio.tests import factories
from goodtablesio.integrations.github.tasks.repos import sync_user_repos
pytestmark = pytest.mark.usefixtures('session_cleanup')


# Tests

def test_sync_user_repos(celery_app, GitHubForIterRepos):
    job = factories.InternalJob()
    user = factories.User(github_oauth_token='my-token')
    sync_user_repos.delay(user.id, job_id=job.id)
    GitHubForIterRepos.assert_called_with(token='my-token')
    sources = sorted(user.sources, key=lambda source: source.name)
    assert sources[0].conf['github_id'] == 'id1'
    assert sources[0].name == 'owner1/repo1'
    assert sources[0].active is True
    assert sources[1].conf['github_id'] == 'id2'
    assert sources[1].name == 'owner2/repo2'
    assert sources[1].active is False
