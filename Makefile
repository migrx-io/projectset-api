#                                                                               
# Commonly used targets (see each target for more information):                 
#   run: Build code.                                                            

SHELL := /usr/bin/env bash                                                      
PYLINT_OPTS=""

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
