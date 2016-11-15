.PHONY: all celery install dev list requirements serve test


all: list

celery:
	celery -A goodtablesio.tasks worker --loglevel=info

dev:
	FLASK_APP=devapp.py FLASK_DEBUG=1 flask run

install:
	pip install --upgrade -r requirements.dev

list:
	@grep '^\.PHONY' Makefile | cut -d' ' -f2- | tr ' ' '\n'

requirements:
	pip-compile > requirements.txt

start:
	python -m goodtablesio.app

test:
	pylama goodtablesio
	py.test
