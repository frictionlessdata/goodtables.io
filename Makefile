.PHONY: help frontend docs docs-watch

.DEFAULT_GOAL := help

PACKAGE := $(shell grep '^PACKAGE =' setup.py | cut -d "'" -f2)
REPOSITORY := 'frictionlessdata/goodtables.io'
SHELL := /bin/bash

help: # http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'



install-backend: ## Install the dependencies for the backend app
	pip3 install --upgrade --no-cache-dir --exists-action w -r requirements.txt

install-dev: ## Install the additional development dependencies for the app
	pip3 install --upgrade --no-cache-dir tox

install-frontend: ## Install the dependencies for frontend development and compilation
	npm install

install: install-backend install-frontend ## Install backend and frontend dependencies

lint-backend: ## Run lint checker on the backend app
	tox -e lint

lint-frontend: ## Run lint checker on frontend app
	npm run lint

lint: lint-backend lint-frontend ## Run all lint checkers

test-unit-backend: ## Run the unit tests for the backend app
	tox

test-unit-frontend: ## Run the unit tests for the frontend app
	npm test

test-unit-frontend-watch: ## Run the unit tests for the frontend app
	npm run test:watch

test-unit: test-unit-backend test-unit-frontend ## Run all tests

test-e2e: ## Run end to end tests
	NODE_ENV=test tox -e e2e

test: lint test-unit test-e2e ## Run all tests

deps: ## Freeze dependencies for the backend app
	pip-compile > requirements.txt

build: ## Build the Docker image for this app
	docker build --tag $(REPOSITORY) --rm=false .

login: ## Login to Docker Hub
	docker login -e $DOCKER_EMAIL -u $DOCKER_USER -p $DOCKER_PASSWORD

push: ## Push the latest Docker image to Docker Hub
	docker push $(REPOSITORY)

shell: ## Run an interactive bash session in the container
	docker run -it $(REPOSITORY) /bin/bash

run: ## Run the container
	docker run $(REPOSITORY)

deploy: build login push ## Build the Docker image and push it to the Docker Hub

migrate: ## Run database migrations for the app
	tox -e migrate

frontend: ## Compile the frontend assets
	npm run build

frontend-dev: ## Compile the frontend assets for development
	npm run build:dev

frontend-watch: ## Compile the frontend assets for development using watch mode
	npm run build:watch

app: ## Serve the app with Gunicorn
	gunicorn goodtablesio.app:app --config gunicorn_settings.py

app-dev: ## Serve the app with Werkzeug
	FLASK_APP=goodtablesio/app.py FLASK_DEBUG=1 flask run

queue: ## Run celery for production
	celery -A goodtablesio.celery_app worker -Q default,internal --loglevel=WARNING

queue-flower: ## Run flower, celery monitoring tool
	celery flower -A goodtablesio.celery_app

queue-dev: ## Run celery for development
	celery -A goodtablesio.celery_app worker -Q default,internal --loglevel=DEBUG

add-admin: ## Give an existing user admin permissions (Usage: make add-admin USERNAME=name_or_id)
	FLASK_APP=goodtablesio/app.py flask add_admin $(USERNAME)

remove-admin: ## Remove admin permissions an existing user (Usage: make remove-admin USERNAME=name_or_id)
	FLASK_APP=goodtablesio/app.py flask remove_admin $(USERNAME)

server: ## Command to run the app as queue or server
	@if [ $(queue_mode) == "1" ]; then \
		make queue; \
	elif [ $(queue_mode) == "2" ]; then \
		make queue-flower; \
	else \
		make migrate; \
		make app; \
	fi

spec:
	wget -O frontend/spec.json https://raw.githubusercontent.com/frictionlessdata/data-quality-spec/master/spec.json

docs:
	tox -e docs

docs-watch:
	tox -e docs-watch
