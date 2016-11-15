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
def validate(payload, task_id=None):
    """Main validation task.

    Args:
        payload (dict): task payload

    Payload structure reflects `goodtables.Inspector` API:
        - `config` key will be used as `Inspector` options
        - all other keys will be used as `Inspector.inspect` options

    Examples:
        - table preset:
            ```
            payload = {
                'source': 'path.csv',
                'config': {
                    'checks': 'structure',
                }
            }
            ```
        - tables preset:
            ```
            payload = {
                'source': [
                    {'source': 'path1.csv'},
                    {
                        'source': 'path2.csv',
                        'schema': 'schema.json',
                        'delimiter': ';',
                    }
                ],
                'preset': 'tables',
                'config': {
                    'checks': 'schema',
                    'error_limit': 10,
                    'order_fields': True,
                }
            }
            ```
        - datapackage preset:
            ```
            payload = {
                'source': 'datapackage.json',
                'preset': 'datapackage',
                'config': {
                    'table_limit': 2,
                }
            }
            ```

    """
    # Get report
    inspector = Inspector(**payload.pop('config', {}))
    report = inspector.inspect(**payload)

    # Save report
    database = dataset.connect(config.DATABASE_URL)
    row = {
        'task_id': task_id or validate.request.id,
        'report': report,
        'finished': datetime.datetime.utcnow()
    }
    database['reports'].update(row,
                               ['task_id'],
                               types={'report': JSONB, 'finished': DateTime},
                               ensure=True)
