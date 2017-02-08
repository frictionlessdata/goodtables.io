from celery import Celery
from goodtablesio import settings


# Module API

celery_app = Celery('tasks')
celery_app.config_from_object(settings)
