from github3 import GitHub


# Module API

def iter_repos_by_token(token):
    """Returns list of repos as list of dicts {id, owner, repo, active}.
    """
    client = GitHub(token=token)
    for repo in client.iter_repos():
        active = False
        data = repo.to_json()
        for hook in repo.iter_hooks():
            if hook.config.get('is_goodtables_hook'):
                active = True
        yield {
            'integration_name': 'github',
            'name': '{0}/{1}'.format(data['owner']['login'], data['name']),
            'conf': {
                'github_id': str(data['id']),
                'private': data['private'],
            },
            'active': active
        }
