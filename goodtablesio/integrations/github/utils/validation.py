from celery import chain
from goodtablesio.tasks.validate import validate
from goodtablesio.integrations.github.tasks.jobconf import get_validation_conf


# Module API

def run_validation(owner, repo, sha, job_id, tokens):
    """Starts validation tasks on queue
    """
    tasks_chain = chain(
        get_validation_conf.s(owner, repo, sha, job_id=job_id, tokens=tokens),
        validate.s(job_id=job_id))
    tasks_chain.delay()
