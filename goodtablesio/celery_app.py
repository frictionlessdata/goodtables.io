import celery
import raven
from raven.contrib.celery import register_signal, register_logger_signal

from goodtablesio import settings


class Celery(celery.Celery):

    def on_configure(self):
        client = raven.Client(settings.SENTRY_DSN)
        register_logger_signal(client)  # defaults to logging.ERROR
        register_signal(client)


app = Celery(__name__)
app.config_from_object(settings)
