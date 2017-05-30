import logging
from github3 import GitHub
log = logging.getLogger(__name__)


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


def get_default_repo_details(owner, repo, token):
    """Return defaults repo details.
    """
    try:
        client = GitHub(token=token)
        repo_client = client.repository(owner, repo)
        branch_client = repo_client.branch(repo_client.default_branch)
        branch_data = branch_client.to_json()
        branch_name = branch_data['name']
        author_name = branch_data['commit']['author']['login']
        commit_message = branch_data['commit']['commit']['message']
        sha = branch_data['commit']['sha']
    except Exception as exception:
        log.exception(exception)
        return None
    return {
        'is_pr': False,
        'owner': owner,
        'repo': repo,
        'sha': sha,
        'branch_name': branch_name,
        'author_name': author_name,
        'commit_message': commit_message,
    }
