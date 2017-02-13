.PHONY: help

.DEFAULT_GOAL := help

PACKAGE := $(shell grep '^PACKAGE =' setup.py | cut -d "'" -f2)
REPOSITORY := 'frictionlessdata/goodtables.io'
SHELL := /bin/bash

help: # http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install: ## install the dependencies for the app
	pip3 install --upgrade pip honcho
	pip3 install --upgrade --no-cache-dir --exists-action w -r requirements.txt

install-dev: ## install the additional development dependencies for the app
	pip3 install --upgrade --no-cache-dir -r requirements.dev

install-frontend: ## install the dependencies for frontend development and compilation
	npm install

release: ## tag a release from master and push to origin
	bash -c '[[ -z `git status -s` ]]'
	git tag -a -m release $(VERSION)
	git push --tags

test: ## run the tests for the app
	py.test --cov goodtablesio --cov-report term-missing

build: ## build the Docker image for this app
	docker build --tag $(REPOSITORY) --rm=false .

login: ## Login to docker hub
	docker login -e $DOCKER_EMAIL -u $DOCKER_USER -p $DOCKER_PASSWORD

push: ## push the latest Docker image to DockerHub
	docker push $(REPOSITORY)

shell: ## run an interactive bash session in the container
	docker run -it $(REPOSITORY) /bin/bash

run: ## run the container
	docker run $(REPOSITORY)

deploy: build login push

migrate: ## run database migrations for the app
	alembic upgrade head

frontend: ## compile the frontend assets
	npm run build:prod

app: ## serve the app with gunicorn
	gunicorn --bind 127.0.0.1:5000 --access-logfile - --log-file - goodtablesio.app:app

app-debug: ## serve the app with werkzueg
	FLASK_APP=goodtablesio/app.py FLASK_DEBUG=1 flask run

queue: ## run celery for production
	celery -A goodtablesio.celery_app worker --loglevel=WARNING

queue-debug: ## run celery for development
	celery -A goodtablesio.celery_app worker --loglevel=DEBUG

server: ## command to run the command as queue or server
	@if [ $(queue_mode) ]; then \
		make queue; \
	else \
		make app; \
	fi
