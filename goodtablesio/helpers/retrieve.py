from goodtablesio import services


# Module API

def get_job(job_id):
    """Get job by identifier.

    Args:
        job_id (str): job identifier

    Returns:
        dict: job result if job was found, None otherwise

    """
    result = services.database['jobs'].find_one(job_id=job_id)

    if not result:
        return None
    # TODO: we need to store the status in the DB as we can no longer rely on
    # the job id being the same one used by a celery task
    status = 'Not Implemented'

    # TODO: this should not be needed after #33
    if 'report' not in result:
        result['report'] = None
    if 'finished' not in result:
        result['finished'] = None

    return {'status': status, 'result': result}


def get_job_ids():
    """Get all job identifiers.

    Returns:
        str[]: list of job identifiers

    """
    return [r['job_id']
            for r in
            services.database['jobs'].find(order_by=['-created'])]
