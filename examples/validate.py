import time
from goodtablesio import helpers


# Start celery
# celery -A goodtablesio.tasks worker --loglevel=info


# Validate
payload = {
    'files': [
        {'source': 'https://raw.githubusercontent.com/frictionlessdata/goodtables-py/master/data/valid.csv'},
        {
            'source': 'https://raw.githubusercontent.com/frictionlessdata/goodtables-py/master/data/invalid.csv',
            # 'schema': ...
            # 'delimiter': ...
            # other options
        },
    ],
    'settings': {
        'checks': 'structure',
        'error_limit': 1,
        # other options
    }
}
task_id = helpers.create_task(payload)
while True:
    time.sleep(1)
    task = helpers.get_task(task_id)
    print(task)
    if task['status'] != 'PENDING':
        break
