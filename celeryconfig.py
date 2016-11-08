import os


# Celery

broker_url = os.environ('BROKER_URL', 'redis://localhost:6379/0')
result_backend = os.environ('RESULT_BACKEND', 'redis://localhost:6379/1')

celery_task_serializer = 'json'
celery_result_serializer = 'json'
celery_timezone = 'Europe/London'
celery_enable_utc = True
