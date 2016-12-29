import pytest
import datetime
from celery import Celery
from goodtablesio import exceptions, models
from goodtablesio.utils.jobtask import JobTask
from goodtablesio.tests import factories
pytestmark = pytest.mark.usefixtures('session_cleanup')


# Tests

def test_JobTask_on_failure_invalid_job_conf():

    # Prepare things
    job = factories.Job(_save_in_db=True)
    app = Celery('app')
    app.conf['task_always_eager'] = True

    # Prepare and call task
    @app.task(base=JobTask)
    def task(job_id):
        raise exceptions.InvalidJobConfiguration()
    task.s(job_id=job.id).delay()

    # Assert errored job
    jobs = models.job.get_all()
    assert len(jobs) == 1

    updated_job = jobs[0]
    assert updated_job['id'] == job.id
    assert updated_job['status'] == 'error'
    assert updated_job['error'] == {'message': 'Invalid job configuration'}
    assert isinstance(updated_job['finished'], datetime.datetime)


def test_JobTask_on_failure_invalid_validation_conf():

    # Prepare things
    job = factories.Job(_save_in_db=True)
    app = Celery('app')
    app.conf['task_always_eager'] = True

    # Prepare and call task
    @app.task(base=JobTask)
    def task(job_id):
        raise exceptions.InvalidValidationConfiguration()
    task.s(job_id=job.id).delay()

    # Assert errored job
    jobs = models.job.get_all()
    assert len(jobs) == 1

    updated_job = jobs[0]
    assert updated_job['id'] == job.id
    assert updated_job['status'] == 'error'
    assert updated_job['error'] == {'message': 'Invalid validation configuration'}
    assert isinstance(updated_job['finished'], datetime.datetime)
