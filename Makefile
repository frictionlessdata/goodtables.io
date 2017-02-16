.PHONY: help

.DEFAULT_GOAL := help

PACKAGE := $(shell grep '^PACKAGE =' setup.py | cut -d "'" -f2)
REPOSITORY := 'frictionlessdata/goodtables.io'
SHELL := /bin/bash

help: # http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'



install-backend: ## Install the dependencies for the backend app
	pip3 install --upgrade pip honcho
	pip3 install --upgrade --no-cache-dir --exists-action w -r requirements.txt

install-dev: ## Install the additional development dependencies for the app
	pip3 install --upgrade --no-cache-dir -r requirements.dev

install-frontend: ## Install the dependencies for frontend development and compilation
	npm install

install: install-backend install-frontend ## Install backend and frontend dependencies

test-backend: ## Run the tests for the backend app
	py.test --cov goodtablesio --cov-report term-missing

test-frontend: ## Run the tests for the frontend app
	npm run test

test: test-backend test-frontend ## Run all tests

spec: ## Run end to end tests
	npm run spec

lint-backend: ## Run lint checker on the backend app
	pylama goodtablesio

lint-frontend: ## Run lint checker on frontend app
	npm run lint

lint: lint-backend lint-frontend ## Run all lint checkers

deps-backend: ## Freeze dependencies for the backend app
	py.deps --cov goodtablesio --cov-report term-missing

deps-frontend: ## Freeze dependencies for the frontend app
	npm run deps

deps: deps-backend deps-frontend ## Freeze all dependencies

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
	alembic upgrade head

frontend: ## Compile the frontend assets
	npm run build:prod

frontend-dev: ## Compile the frontend assets for development
	npm run build:dev

app: ## Serve the app with Gunicorn
	gunicorn goodtablesio.app:app --config server.py

app-dev: ## Serve the app with Werkzeug
	FLASK_APP=goodtablesio/app.py FLASK_DEBUG=1 flask run

queue: ## Run celery for production
	celery -A goodtablesio.celery_app worker --loglevel=WARNING

queue-dev: ## Run celery for development
	celery -A goodtablesio.celery_app worker --loglevel=DEBUG

server: ## Command to run the app as queue or server
	@if [ $(queue_mode) ]; then \
		make queue; \
	else \
		make migrate; \
		make app; \
	fi
