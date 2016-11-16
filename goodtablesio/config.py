import os
import logging
from logging.handlers import SysLogHandler
from dotenv import load_dotenv
load_dotenv('.env')


# General

TABULAR_EXTENSIONS = ['csv', 'xls', 'xlsx', 'ods']

# Database

DATABASE_URL = os.environ['DATABASE_URL']

# Celery

broker_url = os.environ['BROKER_URL']
result_backend = os.environ['RESULT_BACKEND']
task_serializer = 'json'
result_serializer = 'json'
timezone = 'Europe/London'
enable_utc = True

# Logging

logging.basicConfig(level=logging.DEBUG)
if os.environ.get('LOGGING_URL', None):
    root_logger = logging.getLogger()
    host, port = os.environ['LOGGING_URL'].split(':')
    syslog_handler = SysLogHandler(address=(host, int(port)))
    syslog_handler.setLevel(logging.INFO)
    root_logger.addHandler(syslog_handler)
