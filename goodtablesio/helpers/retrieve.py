from goodtablesio import services


# Module API

def get_job(job_id):
    """Get job by identifier.

    Args:
        job_id (str): job identifier

    Returns:
        dict: job result

    """
    report = services.database['reports'].find_one(job_id=job_id)
    # TODO: we need to store the status in the DB as we can no longer rely on
    # the job id being the same one used by a celery task
    status = 'Not Implemented'
    return {'status': status, 'report': report}


def get_job_ids():
    """Get all job identifiers.

    Returns:
        str[]: list of job identifiers

    """
    return [r['job_id']
            for r in
            services.database['reports'].find(order_by=['-created'])]
