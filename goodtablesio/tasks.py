import datetime
import logging

import dataset
from celery import Celery
from sqlalchemy.types import DateTime
from sqlalchemy.dialects.postgresql import JSONB
from goodtables import Inspector

from . import config


log = logging.getLogger(__name__)


# Module API

app = Celery('tasks')
app.config_from_object(config)

# TODO: automate
app.autodiscover_tasks(['goodtablesio.plugins.github'])


@app.task(name='goodtablesio.tasks.validate')
def validate(validation_conf, job_id=None):
    """Main validation task.

    Args:
        validation_conf (dict): validation configuration

    See `schemas/validation-conf.yml`.

    """
    # Get report
    settings = validation_conf.get('settings', {})
    inspector = Inspector(**settings)
    report = inspector.inspect(validation_conf['files'], preset='tables')

    # Save report
    database = dataset.connect(config.DATABASE_URL)
    row = {
        'job_id': job_id or validate.request.id,
        'report': report,
        'finished': datetime.datetime.utcnow()
    }
    database['jobs'].update(row,
                            ['job_id'],
                            types={'report': JSONB, 'finished': DateTime},
                            ensure=True)
