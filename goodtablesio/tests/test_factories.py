import pytest

from goodtablesio import services
from goodtablesio.models.job import Job
from goodtablesio.tests import factories

pytestmark = pytest.mark.usefixtures('db_cleanup')


def test_create_job():
    job = factories.Job()

    job_db = services.db_session.query(Job).get(job.job_id)

    assert job_db.job_id == job.job_id


def test_build_job():
    job = factories.Job.build()

    job_db = services.db_session.query(Job).get(job.job_id)

    assert job_db is None


def test_create_job_are_different():

    job1 = factories.Job()
    job2 = factories.Job()

    assert job1.job_id != job2.job_id

    assert job1.created != job2.created


def test_create_job_overrides():
    job = factories.Job(job_id='my-id', report={'a': 'b'})

    assert job.job_id == 'my-id'
    assert job.report == {'a': 'b'}
