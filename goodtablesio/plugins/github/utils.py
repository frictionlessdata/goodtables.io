import logging

import requests

from goodtablesio import config

log = logging.getLogger(__name__)


# Module API

def set_commit_status(state, owner, repo, sha, job_id):

    url = '{base}/repos/{owner}/{repo}/statuses/{sha}'.format(
        base=config.GITHUB_API_BASE,
        owner=owner, repo=repo, sha=sha,
    )

    headers = {
        'Authorization': 'token {0}'.format(config.GITHUB_API_TOKEN),
    }

    if state == 'pending':
        description = 'Data validation under way'
    elif state == 'success':
        description = 'Data is valid'
    elif state == 'failure':
        description = 'Data is invalid'
    elif state == 'error':
        description = 'Errors during data validation'
    else:
        raise ValueError('Wrong Github Status state: {0}'.format(state))

    data = {
      'state': state,
      'target_url': '{base}/job/{job_id}'.format(
           base=config.BASE_URL, job_id=job_id),
      'description': description,
      'context': 'goodtables.io/push'
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 201:
        return True
    else:
        log.error('There was an error setting the GitHub status: ' +
                  '{url} {response} {job_id} {state}'.format(
                      url=url, response=response.text,
                      job_id=job_id, state=state))
        return False
