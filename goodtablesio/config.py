import os
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
