from github3 import GitHub
from goodtablesio import settings


# Module API

def activate_hook(token, owner, repo):
    """Activate goodtables hook for GitHub repo.
    """
    name = 'web'
    config = {
        'content_type': 'json',
        'secret': settings.GITHUB_HOOK_SECRET,
        # We can't use url_for here because there is no app context
        'url': '%s/github/hook' % settings.BASE_URL,
    }
    events = [
        'pull_request',
        'push',
    ]
    client = GitHub(token=token)
    repo = client.repository(owner, repo)
    repo.create_hook(name, config=config, events=events)


def deactivate_hook(token, owner, repo):
    """Deactivate goodtables hook for GitHub repo.
    """
    client = GitHub(token=token)
    repo = client.repository(owner, repo)
    for hook in repo.iter_hooks():
        # TODO: improve this logic?
        if 'goodtables' in hook.config.get('url', ''):
            hook.delete()


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
