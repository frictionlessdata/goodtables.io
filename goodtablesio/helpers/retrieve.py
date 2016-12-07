from goodtablesio.services import db_session
from goodtablesio.models import Job


# Module API

def get_job(job_id):
    """Get job by identifier.

    Args:
        job_id (str): job identifier

    Returns:
        dict: job result if job was found, None otherwise

    """
    job = db_session.query(Job).get(job_id)

    if not job:
        return None

    return job.to_dict()


def get_job_ids():
    """Get all job identifiers.

    Returns:
        str[]: list of job identifiers

    """

    job_ids = db_session.query(Job.job_id).order_by(Job.created.desc()).all()
    return [r.job_id for r in job_ids]
