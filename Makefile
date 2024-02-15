#                                                                               
# Commonly used targets (see each target for more information):                 
#   run: Build code.                                                            

SHELL := /usr/bin/env bash                                                      

.PHONY: all
all: help

.PHONY: help
help:
	@echo "make tests - run tests"
	@echo "make run - run"

.PHONY: run
run:
	PORT=8082 PYENV=${PYENV} ./start
