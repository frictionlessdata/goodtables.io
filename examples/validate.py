import time
from goodtablesio import handlers


# Start celery
# celery -A goodtablesio.tasks worker --loglevel=info


# Validate table
print('Table:')
payload = {
    'source': 'https://raw.githubusercontent.com/frictionlessdata/goodtables-py/master/data/valid.csv',
}
task_id = handlers.post_task(payload)
while True:
    time.sleep(1)
    task = handlers.get_task(task_id)
    print(task)
    if task['status'] != 'PENDING':
        break


# Validate tables
print('Tables:')
payload = {
    'source': [
        {'source': 'https://raw.githubusercontent.com/frictionlessdata/goodtables-py/master/data/valid.csv'},
        {
            'source': 'https://raw.githubusercontent.com/frictionlessdata/goodtables-py/master/data/invalid.csv',
            # 'schema': ...
            # 'delimiter': ...
            # other options
        },
    ],
    'preset': 'tables',
    'config': {
        'checks': 'structure',
        'error_limit': 1,
        # other options
    }
}
task_id = handlers.post_task(payload)
while True:
    time.sleep(1)
    task = handlers.get_task(task_id)
    print(task)
    if task['status'] != 'PENDING':
        break


# Validate datapackage
print('Datapackage:')
payload = {
    'source': 'https://raw.githubusercontent.com/frictionlessdata/goodtables-py/master/data/datapackages/valid/datapackage.json',
    'preset': 'datapackage',
}
task_id = handlers.post_task(payload)
while True:
    time.sleep(1)
    task = handlers.get_task(task_id)
    print(task)
    if task['status'] != 'PENDING':
        break
