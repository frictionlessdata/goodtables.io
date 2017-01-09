import pytest
from unittest.mock import Mock, patch
from goodtablesio.plugins.github.utils.repos import iter_repos_by_token


# Tests

def test_iter_repos_by_token(GitHubForIterRepos):
    repos = list(iter_repos_by_token('TOKEN'))
    GitHubForIterRepos.assert_called_with(token='TOKEN')
    assert repos == [
        {
            'id': 'id1',
            'owner': 'owner1',
            'repo': 'repo1',
            'active': True,
        },
        {
            'id': 'id2',
            'owner': 'owner2',
            'repo': 'repo2',
            'active': False,
        },
    ]


# Fixtures

@pytest.fixture
def GitHubForIterRepos():
    GitHub = patch('goodtablesio.plugins.github.utils.repos.GitHub').start()
    repo1 = Mock(to_json=Mock(return_value={
        'id': 'id1',
        'name': 'repo1',
        'owner': {
            'login': 'owner1',
        }
    }))
    hook1 = Mock(config=Mock(get=Mock(return_value='http://goodtables.io')))
    repo1.iter_hooks.return_value = [hook1]
    repo2 = Mock(to_json=Mock(return_value={
        'id': 'id2',
        'name': 'repo2',
        'owner': {
            'login': 'owner2',
        }
    }))
    hook2 = Mock(config=Mock(get=Mock(return_value='http://example.com')))
    repo2.iter_hooks.return_value = [hook2]
    GitHub.return_value.iter_repos.return_value = [repo1, repo2]
    yield GitHub
    patch.stopall()
