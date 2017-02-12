.PHONY: help

.DEFAULT_GOAL := help

PACKAGE := $(shell grep '^PACKAGE =' setup.py | cut -d "'" -f2)
REPOSITORY := 'frictionlessdata/goodtables.io'

help: # http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install: ## install the dependencies for the app
	pip3 install --upgrade pip honcho
	pip3 install --upgrade --no-cache-dir --exists-action w -r requirements.txt

install-dev: ## install the additional development dependencies for the app
	pip3 install --upgrade --no-cache-dir pylama tox
	npm install

release: ## tag a release from master and push to origin
	bash -c '[[ -z `git status -s` ]]'
	git tag -a -m release $(VERSION)
	git push --tags

test: ## run the tests for the app
	@echo "goodtables.io tests!"

build: ## build the Docker image for this app
	docker build --tag $(REPOSITORY) --rm=false .

push: ## push the latest Docker image to DockerHub
	docker push $(REPOSITORY)

shell: ## run an interactive bash session in the container
	docker run -it $(REPOSITORY) /bin/bash

migrate: ## run database migrations for the app
	alembic upgrade head

frontend: ## compile the frontend assets
	npm run build:prod

server: ## serve the app with gunicorn
	gunicorn --access-logfile - --log-file - goodtablesio.app:app

server-debug: ## server the app with werkzueg
	FLASK_APP=goodtablesio/app.py FLASK_DEBUG=1 flask run

queue: ## run celery for production
	celery -A goodtablesio.celery_app worker --loglevel=WARNING

queue-debug: ## run celery for development
	celery -A goodtablesio.celery_app worker --loglevel=DEBUG
