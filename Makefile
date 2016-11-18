.PHONY: all celery celery-dev dev install list requirements serve test


all: list

celery:
	celery -A goodtablesio.tasks worker --loglevel=info

celery-dev:
	celery -A goodtablesio.tasks worker --loglevel=debug

dev:
	FLASK_APP=goodtablesio/app.py FLASK_DEBUG=1 flask run

install:
	pip install --upgrade -r requirements.dev

list:
	@grep '^\.PHONY' Makefile | cut -d' ' -f2- | tr ' ' '\n'

requirements:
	pip-compile > requirements.txt

start:
	gunicorn --access-logfile - --log-file - goodtablesio.app:app

test:
	pylama goodtablesio
	py.test --cov goodtablesio --cov-report term-missing
