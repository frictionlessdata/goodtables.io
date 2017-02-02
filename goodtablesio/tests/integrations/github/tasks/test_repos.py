import pytest
from goodtablesio.tests import factories
from goodtablesio.integrations.github.tasks.repos import sync_user_repos
pytestmark = pytest.mark.usefixtures('session_cleanup')


# Tests

def test_sync_user_repos(GitHubForIterRepos):
    token = 'TOKEN'
    user = factories.User()
    sync_user_repos(user.id, token)
    GitHubForIterRepos.assert_called_with(token=token)
    assert user.projects[0].conf['github_id'] == 'id1'
    assert user.projects[0].name == 'owner1/repo1'
    assert user.projects[0].active is True
    assert user.projects[1].conf['github_id'] == 'id2'
    assert user.projects[1].name == 'owner2/repo2'
    assert user.projects[1].active is False
