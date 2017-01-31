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
    assert user.github_repos[0].id == 'id1'
    assert user.github_repos[0].owner == 'owner1'
    assert user.github_repos[0].repo == 'repo1'
    assert user.github_repos[0].active is True
    assert user.github_repos[1].id == 'id2'
    assert user.github_repos[1].owner == 'owner2'
    assert user.github_repos[1].repo == 'repo2'
    assert user.github_repos[1].active is False
