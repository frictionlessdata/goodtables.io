from goodtablesio.services import db_session as default_db_session
from goodtablesio.models import Job


def update_job(params, _db_session=None):
    """
    Updates a job object in the database.

    Arguments:
        params (dict): A dictionary with the fields to be updated. It must
            contain a valid `job_id` key.
        _db_session (Session): An alternative SQLAlchemy session instance. If
            not provided the default one from goodtablesio.services will be
            used. This is useful for tasks run on the Celery processes.

    Returns:
        job_id (str): The updated job identifier

    Raises:
        ValueError: A `job_id` was not provided in the params dict.
    """

    job_id = params.get('job_id')
    if not job_id:
        raise ValueError('You must provide a job_id in the params dict')

    db_session = _db_session or default_db_session

    db_session.query(Job).filter(Job.job_id == job_id).update(params)
    db_session.commit()

    return job_id
