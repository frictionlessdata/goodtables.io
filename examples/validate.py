import time
from goodtablesio import handlers


# Start celery
# celery -A goodtablesio.tasks worker --loglevel=info


# Validate table
payload = {
    'source': 'https://raw.githubusercontent.com/frictionlessdata/goodtables-py/master/data/valid.csv',
}
task_id = handlers.post_task(payload)
time.sleep(5)
task = handlers.get_task(task_id)
print(task)
