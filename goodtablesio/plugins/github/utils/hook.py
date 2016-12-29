# Module API


def get_owner_repo_sha_from_hook_payload(payload):
    """Return tuple (owner, repo, sha) from GitHub hook payload.
    """

    try:

        # PR
        if payload.get('pull_request'):
            if payload['action'] != 'opened':
                return None, None, None
            repo = payload['pull_request']['head']['repo']['name']
            owner = payload['pull_request']['head']['repo']['owner']['login']
            sha = payload['pull_request']['head']['sha']

        # PUSH
        else:
            repo = payload['repository']['name']
            owner = payload['repository']['owner']['name']
            sha = payload['head_commit']['id']

    except KeyError:
        return None, None, None

    return owner, repo, sha
