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
            # TODO: improve this logic?
            if 'goodtables' in hook.config.get('url', ''):
                active = True
        yield {
            'id': str(data['id']),
            'owner': data['owner']['login'],
            'repo': data['name'],
            'active': active,
        }
