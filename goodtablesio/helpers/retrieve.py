from goodtablesio import services


# Module API

def get_job(job_id):
    """Get job by identifier.

    Args:
        job_id (str): job identifier

    Returns:
        dict: job result if job was found, None otherwise

    """
    job = services.database['jobs'].find_one(job_id=job_id)

    if not job:
        return None

    # TODO: this should not be needed after #33
    if 'report' not in job:
        job['report'] = None
    if 'finished' not in job:
        job['finished'] = None

    return job


def get_job_ids():
    """Get all job identifiers.

    Returns:
        str[]: list of job identifiers

    """
    return [r['job_id']
            for r in
            services.database['jobs'].find(order_by=['-created'])]
