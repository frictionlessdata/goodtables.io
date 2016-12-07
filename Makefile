.PHONY: all celery celery-dev install list migrate requirements server-dev server test


all: list

celery:
	celery -A goodtablesio.tasks worker --loglevel=info

celery-dev:
	celery -A goodtablesio.tasks worker --loglevel=debug

install:
	pip install --upgrade -r requirements.dev

list:
	@grep '^\.PHONY' Makefile | cut -d' ' -f2- | tr ' ' '\n'

migrate:
	alembic upgrade head

requirements:
	pip-compile > requirements.txt

server:
	gunicorn --access-logfile - --log-file - goodtablesio.app:app

server-dev:
	FLASK_APP=goodtablesio/app.py FLASK_DEBUG=1 flask run

test:
	pylama goodtablesio
	py.test --cov goodtablesio --cov-report term-missing
