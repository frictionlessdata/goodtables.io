from celery import Celery
from goodtables import Inspector


app = Celery('tasks')
app.config_from_object('celeryconfig')


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
