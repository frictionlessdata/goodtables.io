broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/1'

celery_task_serializer = 'json'
celery_result_serializer = 'json'
celery_timezone = 'Europe/London'
celery_enable_utc = True
