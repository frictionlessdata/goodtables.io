from celery import Celery
from goodtables import Inspector


app = Celery('tasks')
app.config_from_object('celeryconfig')


@app.task(name='goodtableio.tasks.validate')
def validate(user_id, job_id, job):
    """Main validation task.

    Args:
        user_id (str): user identifier
        job_id (str): job identifier
        job (mixed): validation job descriptor

    """

    # TODO: Process multiple files in batch
    # TODO: Configure inspector (schemas, checks, etc)

    inspector = Inspector()
    report = inspector.inspect(url)

    # TODO: Upload report

    return report
