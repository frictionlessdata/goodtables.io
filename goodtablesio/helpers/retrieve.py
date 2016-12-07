from goodtablesio.services import db_session as default_db_session
from goodtablesio.models import Job


# Module API

def get_job(job_id, _db_session=None):
    """
    Get a job object in the database and return it as a dict.

    Arguments:
        job_id (str): The job id.
        _db_session (Session): An alternative SQLAlchemy session instance. If
            not provided the default one from goodtablesio.services will be
            used. This is useful for tasks run on the Celery processes.

    Returns:
        job (dict): A dictionary with the job details, or None if the job was
            not found.
    """

    db_session = _db_session or default_db_session

    job = db_session.query(Job).get(job_id)

    if not job:
        return None

    return job.to_dict()


def get_job_ids(_db_session=None):
    """Get all job ids from the database.

    Arguments:
        _db_session (Session): An alternative SQLAlchemy session instance. If
            not provided the default one from goodtablesio.services will be
            used. This is useful for tasks run on the Celery processes.

    Returns:
        job_ids (str[]): A list of job ids, sorted by descdendig creation date.

    """

    db_session = _db_session or default_db_session

    job_ids = db_session.query(Job.job_id).order_by(Job.created.desc()).all()
    return [j.job_id for j in job_ids]


def get_jobs(_db_session=None):
    """Get all jobs in the database as dict.

    Warning: Use with caution, this should probably only be used in tests

    Arguments:
        _db_session (Session): An alternative SQLAlchemy session instance. If
            not provided the default one from goodtablesio.services will be
            used. This is useful for tasks run on the Celery processes.

    Returns:
        jobs (dict[]): A list of job dicts, sorted by descending creation date.

    """

    db_session = _db_session or default_db_session

    jobs = db_session.query(Job).order_by(Job.created.desc()).all()
    return [j.to_dict() for j in jobs]
