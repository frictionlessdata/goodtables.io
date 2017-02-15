"""gunicorn configuration file."""
import os


debug = os.getenv('DEBUG')
bind = "0.0.0.0:5000"
accesslog = '-'
errorlog = '-'
loglevel = 'error'
workers = 8

