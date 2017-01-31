import pytest
from unittest.mock import Mock, patch


# Fixtures

@pytest.fixture
def GitHubForIterRepos():
    GitHub = patch('goodtablesio.integrations.github.utils.repos.GitHub').start()
    repo1 = Mock(to_json=Mock(return_value={
        'id': 'id1',
        'name': 'repo1',
        'owner': {
            'login': 'owner1',
        }
    }))
    hook1 = Mock(config=Mock(get=Mock(return_value=True)))
    repo1.iter_hooks.return_value = [hook1]
    repo2 = Mock(to_json=Mock(return_value={
        'id': 'id2',
        'name': 'repo2',
        'owner': {
            'login': 'owner2',
        }
    }))
    hook2 = Mock(config=Mock(get=Mock(return_value=False)))
    repo2.iter_hooks.return_value = [hook2]
    GitHub.return_value.iter_repos.return_value = [repo1, repo2]
    yield GitHub
    patch.stopall()
