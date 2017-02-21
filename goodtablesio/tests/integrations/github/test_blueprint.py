import json
from unittest.mock import patch

import pytest

from goodtablesio import models, settings
from goodtablesio.utils.signature import create_signature
from goodtablesio.tests import factories


pytestmark = pytest.mark.usefixtures('session_cleanup')

# TODO: this test should not rely on external HTTP calls to GitHub


@patch('goodtablesio.integrations.github.utils.status.set_commit_status')
def test_create_job(set_commit_status, client, celery_app):

    # TODO: refactor to not use actual calls!
    user = factories.User(github_oauth_token=settings.GITHUB_API_TOKEN)
    factories.GithubRepo(name='frictionlessdata/goodtables.io-example',
                         users=[user])

    data = json.dumps({
        'repository': {
            'name': 'goodtables.io-example',
            'owner': {'name': 'frictionlessdata'},
        },
        'head_commit': {'id': 'd5be243487d9882d7f762e7fa04b36b900164a59'},
    })
    sig = create_signature(settings.GITHUB_HOOK_SECRET, data)
    res = client.post(
        '/github/hook',
        headers={'X-Hub-Signature': sig},
        content_type='application/json',
        data=data)
    job_id = json.loads(res.get_data(as_text=True))['job_id']
    job = models.job.get(job_id)
    assert job['id'] == job_id
    assert job['created']
    assert job['finished']
    assert job['status'] == 'failure'
    assert job['report']
