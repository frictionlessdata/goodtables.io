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
        'is_goodtables_hook': True,
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
        if hook.config.get('is_goodtables_hook'):
            hook.delete()


def get_details_from_hook_payload(payload):
    """Return a dict with details from GitHub hook payload.
    """
    details = {}
    try:

        # PR
        if payload.get('pull_request'):
            if payload['action'] != 'opened':
                return {}

            pull_request = payload['pull_request']

            details['is_pr'] = True
            details['repo'] = pull_request['head']['repo']['name']
            details['owner'] = pull_request['head']['repo']['owner']['login']
            details['sha'] = pull_request['head']['sha']
            details['base_owner'] = (
                pull_request['base']['repo']['owner']['login'])
            details['base_repo'] = pull_request['base']['repo']['name']
            details['pr_number'] = pull_request['number']
            details['pr_title'] = pull_request['title']
            details['author_name'] = pull_request['user']['login']

        # PUSH
        else:
            details['is_pr'] = False
            details['repo'] = payload['repository']['name']
            details['owner'] = payload['repository']['owner']['name']
            details['sha'] = payload['head_commit']['id']
            details['commit_message'] = payload['head_commit']['message']
            details['author_name'] = payload['head_commit']['author']['name']
            details['branch_name'] = payload['ref'].replace('refs/head/', '')

    except KeyError:
        return None

    return details


def get_tokens_for_job(job):
    return [user.github_oauth_token
            for user in job.source.users if user.github_oauth_token]
