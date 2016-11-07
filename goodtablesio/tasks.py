import os

from celery import Celery

from goodtables import Inspector


app = Celery('tasks')
app.config_from_object('celeryconfig')

for key in ('BROKER_URL', 'RESULT_BACKEND'):
    if key in os.environ:
        app.conf.update({key.lower(): os.environ[key]})


@app.task(name='goodtableio.tasks.validate_table')
def validate_table(url):
    '''
    Main validation task

    TODO: Document
    '''

    # TODO: Process multiple files in batch
    # TODO: Configure inspector (schemas, checks, etc)

    inspector = Inspector()
    report = inspector.inspect(url)

    # TODO: Upload report

    return report
