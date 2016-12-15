import logging
import datetime

from sqlalchemy import Column, Unicode, DateTime, update as db_update
from sqlalchemy.dialects.postgresql import JSONB

from goodtablesio.services import database
from goodtablesio.models.base import Base, BaseModelMixin, make_uuid


log = logging.getLogger(__name__)


class Job(Base, BaseModelMixin):

    __tablename__ = 'jobs'

    id = Column(Unicode, primary_key=True, default=make_uuid)
    status = Column(Unicode, default='created')
    plugin_name = Column(Unicode, default='api')
    plugin_conf = Column(JSONB)
    created = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    finished = Column(DateTime(timezone=True))
    report = Column(JSONB)
    error = Column(JSONB)


def create(params):
    """
    Creates a job object in the database.

    Arguments:
        params (dict): A dictionary with the values for the new job.

    Returns:
        job (dict): The newly created job as a dict
    """

    job = Job(**params)

    database['session'].add(job)
    database['session'].commit()

    log.debug('Created job "%s" on the database', job.id)
    return job.to_dict()


def update(params):
    """
    Updates a job object in the database.

    Arguments:
        params (dict): A dictionary with the fields to be updated. It must
            contain a valid `job_id` key.

    Returns:
        job (dict): The updated job as a dict

    Raises:
        ValueError: A `job_id` was not provided in the params dict.
    """

    job_id = params.get('id')
    if not job_id:
        raise ValueError('You must provide a id in the params dict')

    job = database['session'].query(Job).get(job_id)
    if not job:
        raise ValueError('Job not found: %s', job_id)

    job_table = Job.__table__
    u = db_update(job_table).where(job_table.c.id == job_id).values(**params)

    database['session'].execute(u)
    database['session'].commit()

    log.debug('Updated job "%s" on the database', job_id)
    return job.to_dict()


def get(job_id):
    """
    Get a job object in the database and return it as a dict.

    Arguments:
        job_id (str): The job id.

    Returns:
        job (dict): A dictionary with the job details, or None if the job was
            not found.
    """

    job = database['session'].query(Job).get(job_id)

    if not job:
        return None

    return job.to_dict()


def get_ids():
    """Get all job ids from the database.

    Returns:
        job_ids (str[]): A list of job ids, sorted by descending creation date.

    """

    job_ids = database['session'].query(Job.id).order_by(Job.created.desc()).all()
    return [j.id for j in job_ids]


def get_all():
    """Get all jobs in the database as dict.

    Warning: Use with caution, this should probably only be used in tests

    Returns:
        jobs (dict[]): A list of job dicts, sorted by descending creation date.

    """

    jobs = database['session'].query(Job).order_by(Job.created.desc()).all()
    return [j.to_dict() for j in jobs]
