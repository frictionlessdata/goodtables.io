.PHONY: help frontend

.DEFAULT_GOAL := help

export PATH := $(PATH):./node_modules/.bin

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

lint-backend: ## Run lint checker on the backend app
	pylama goodtablesio

lint-frontend: ## Run lint checker on frontend app
	eslint --ext js,vue frontend

lint: lint-backend lint-frontend ## Run all lint checkers

test-unit-backend: ## Run the unit tests for the backend app
	py.test --cov goodtablesio --cov-report term-missing

test-unit-frontend: ## Run the unit tests for the frontend app
	NODE_ENV=testing karma start

test-unit: test-unit-backend test-unit-frontend ## Run all tests

test-e2e: ## Run end to end tests
	NODE_ENV=testing node rune2e.js

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
	alembic upgrade head

frontend: ## Compile the frontend assets
	NODE_ENV=production webpack --progress --hide-modules

frontend-dev: ## Compile the frontend assets for development
	webpack --output-pathinfo --progress --hide-modules

app: ## Serve the app with Gunicorn
	gunicorn goodtablesio.app:app --config server.py --loglevel warning

app-dev: ## Serve the app with Werkzeug
	FLASK_APP=goodtablesio/app.py FLASK_DEBUG=1 flask run

app-e2e: ## Serve the app for e2e with Werkzeug
	FLASK_APP=goodtablesio/app.py FLASK_DEBUG=1 BASE_URL=http://localhost:9999 flask run -p 9999

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
