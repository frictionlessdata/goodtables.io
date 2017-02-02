from goodtablesio.integrations.github.utils.repos import iter_repos_by_token


# Tests

def test_iter_repos_by_token(GitHubForIterRepos):
    token = 'TOKEN'
    repos = list(iter_repos_by_token(token))
    GitHubForIterRepos.assert_called_with(token=token)
    assert repos == [
        {
            'active': True,
            'conf': {'github_id': 'id1'},
            'integration_name': 'github',
            'name': 'owner1/repo1'
        },
        {
            'active': False,
            'conf': {'github_id': 'id2'},
            'integration_name': 'github',
            'name': 'owner2/repo2'
        }
    ]
