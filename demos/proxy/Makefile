SHELL=/bin/bash
PYTHON ?= python
PIP ?= pip
FLAKE8 ?= flake8

all: help

help:
	@echo "  requirements - Install requirements"
	@echo "  flake        - Run flake8 on the source code."
	@echo "  clean        - Clean temp python files."

lint: flake

flake:
	$(FLAKE8) app

clean:
	-find . -type f -a \( -name "*.pyc" -o -name "*$$py.class" \) | xargs rm
	-find . -type d -name "__pycache__" | xargs rm -r

.PHONY: requirements
requirements:
	$(PIP) install --upgrade pip;\
	$(PIP) install -r requirements.txt

