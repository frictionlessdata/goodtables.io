import pytest
from goodtablesio import settings
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
        },
        'private': False
    }))
    hook1 = Mock(config={'url': settings.GITHUB_HOOK_URL})
    repo1.iter_hooks.return_value = [hook1]
    repo2 = Mock(to_json=Mock(return_value={
        'id': 'id2',
        'name': 'repo2',
        'owner': {
            'login': 'owner2',
        },
        'private': False
    }))
    hook2 = Mock(config={'url': 'http://example.com'})
    repo2.iter_hooks.return_value = [hook2]
    repo3 = Mock(to_json=Mock(return_value={
        'id': 'id3',
        'name': 'repo3',
        'owner': {
            'login': 'owner2',
        },
        'private': True
    }))
    hook3 = Mock(config={})
    repo3.iter_hooks.return_value = [hook3]

    GitHub.return_value.iter_repos.return_value = [repo1, repo2, repo3]
    yield GitHub
    patch.stopall()
