from goodtablesio.plugins.github.utils.repos import iter_repos_by_token


# Tests

def test_iter_repos_by_token(GitHubForIterRepos):
    token = 'TOKEN'
    repos = list(iter_repos_by_token(token))
    GitHubForIterRepos.assert_called_with(token=token)
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
