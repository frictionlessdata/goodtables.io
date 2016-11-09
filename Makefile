.PHONY: all install list requirements test


all: list

install:
	pip install --upgrade -r requirements.dev

list:
	@grep '^\.PHONY' Makefile | cut -d' ' -f2- | tr ' ' '\n'

requirements:
	pip-compile > requirements.txt

test:
	pylama goodtablesio
	py.test
