from dotenv import load_dotenv
load_dotenv('.env')


# Celery

broker_url = os.environ['BROKER_URL']
result_backend = os.environ['RESULT_BACKEND']

celery_task_serializer = 'json'
celery_result_serializer = 'json'
celery_timezone = 'Europe/London'
celery_enable_utc = True
