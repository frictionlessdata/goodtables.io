import time
from goodtablesio import helpers


# Start celery
# celery -A goodtablesio.tasks worker --loglevel=info


# Validate
validation_conf = {
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
job_id = helpers.create_and_run_job(validation_conf)
while True:
    time.sleep(1)
    job = helpers.get_job(job_id)
    print(job)
    if job['status'] != 'PENDING':
        break
