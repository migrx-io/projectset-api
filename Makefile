#                                                                               
# Commonly used targets (see each target for more information):                 
#   run: Build code.                                                            

SHELL := /usr/bin/env bash                                                      
PYLINT_OPTS="C0114,C0116,C0115,W0719,R0903,W0718,C0413,C0411,C0209,R0915,R0801"
VERSION=0.1.0

.PHONY: all
all: help

.PHONY: help
help:
	@echo "make tests - run tests"
	@echo "make run - run"

.PHONY: run
run:
	PORT=8082 PYENV=${PYENV} ./start

.PHONY: tests
tests:
	find . -type f -name "*.py" |xargs ${PYENV}/python3 -m yapf -i
	find . -type f -name "*.py" |xargs ${PYENV}/python3 -m pylint --unsafe-load-any-extension=y --disable ${PYLINT_OPTS}

.PHONY: docker-build
docker-build:
	docker build -t projectset-api:${VERSION} .

.PHONY: docker-push
docker-push:
	docker push projectset-api:${VERSION}


