import uuid
from unittest import mock

import pytest

from goodtablesio import tasks, services, helpers


pytestmark = pytest.mark.usefixtures('db_cleanup')


@mock.patch('goodtables.inspector.Inspector.inspect')
def test_tasks_validate(_inspect):

    job_id = str(uuid.uuid4())
    helpers.insert_job_row(job_id)

    mock_report = {'valid': True, 'errors': []}
    _inspect.return_value = mock_report

    validation_conf = {'files': ['file1', 'file2'], 'settings': {}}
    tasks.validate(validation_conf, job_id=job_id)

    _inspect.assert_called_with(validation_conf['files'], preset='tables')

    jobs = [job for job in services.database['jobs'].find()]

    assert len(jobs) == 1

    job = jobs[0]

    assert job['job_id'] == job_id
    assert job['report'] == mock_report
