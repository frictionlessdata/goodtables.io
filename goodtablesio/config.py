import os
import logging
from logging.handlers import SysLogHandler
from dotenv import load_dotenv
load_dotenv('.env')


# Logging

logging.basicConfig(level=logging.DEBUG)
if os.environ.get('LOGGING_URL', None):
    root_logger = logging.getLogger()
    host, port = os.environ['LOGGING_URL'].split(':')
    syslog_handler = SysLogHandler(address=(host, int(port)))
    syslog_handler.setLevel(logging.INFO)
    root_logger.addHandler(syslog_handler)
log = logging.getLogger(__name__)

# General

BASE_URL = os.environ['BASE_URL']
TABULAR_EXTENSIONS = ['csv', 'xls', 'xlsx', 'ods']

# Database

if not os.environ.get('TESTING'):
    log.debug('Not testing mode')
    DATABASE_URL = os.environ['DATABASE_URL']
else:
    log.debug('Testing mode')
    DATABASE_URL = os.environ['TEST_DATABASE_URL']

# Celery

broker_url = os.environ['BROKER_URL']
task_serializer = 'json'
result_serializer = 'json'
timezone = 'Europe/London'
enable_utc = True

# GitHub

GITHUB_API_BASE = 'https://api.github.com'
GITHUB_API_TOKEN = os.environ['GITHUB_API_TOKEN']
# https://developer.github.com/webhooks/securing/
# GITHUB_WEBHOOK_SECRET = os.environ['GITHUB_WEBHOOK_SECRET']
GITHUB_CLONE_DIR = '/tmp'
