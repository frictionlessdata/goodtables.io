from unittest import mock

import pytest
from celery import Celery

from goodtablesio import tasks, services, exceptions
from goodtablesio.tests import factories


pytestmark = pytest.mark.usefixtures('db_cleanup')


@mock.patch('goodtables.inspector.Inspector.inspect')
def test_tasks_validate(_inspect):

    job = factories.Job()

    mock_report = {'valid': True, 'errors': []}
    _inspect.return_value = mock_report

    # Needed to initialize the DB connection
    tasks.init_worker()

    validation_conf = {'files': ['file1', 'file2'], 'settings': {}}
    tasks.validate(validation_conf, job_id=job.job_id)

    _inspect.assert_called_with(validation_conf['files'], preset='tables')

    jobs = [row for row in services.database['jobs'].find()]

    assert len(jobs) == 1

    assert jobs[0]['job_id'] == job.job_id
    assert jobs[0]['report'] == mock_report


def test_JobTask_on_failure():

    # Prepare things
    job = factories.Job()
    tasks.init_worker()
    app = Celery('app')
    app.conf['task_always_eager'] = True

    # Prepare and call task
    @app.task(base=tasks.JobTask)
    def task(job_id):
        raise exceptions.InvalidJobConfiguration()
    task.s(job_id=job.job_id).delay()

    # Assert errored job
    jobs = list(services.database['jobs'].find())
    assert len(jobs) == 1
    assert jobs[0]['job_id'] == job.job_id
    assert jobs[0]['status'] == 'error'
    assert jobs[0]['error'] == {'message': 'Invalid job configuration'}
    assert jobs[0]['finished']
