from celery import Celery
from goodtablesio import settings


# Module API

celery_app = Celery('tasks')
celery_app.config_from_object(settings)

# TODO: automate
celery_app.autodiscover_tasks(['goodtablesio.plugins.github'])
