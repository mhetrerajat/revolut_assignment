# Makefile for common commands

PYTHON=pipenv run python
PROJECT_HOME?=.
DOCKER_IMAGE=revolut_assignment
DOCKER_CONTAINER=revolut_api

.DEFAULT: help

help:
	@echo "make test - To run test cases"
	@echo "make pretty - Does linting and deletes *.pyc files"
	@echo "make requirements - Makes requirements.txt"
	@echo "make testdeploy - Build and deploy docker container"
	@echo "make nest - Short cut to run nest parser cli" 

pretty:
	find . -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	isort -rc --atomic $(PROJECT_HOME)
	find . -type f -name "*.py" -exec $(PYTHON) -m yapf --recursive --parallel --in-place --verbose --style=pep8 {} \;
	find . -type f -name "*.py" -exec $(PYTHON) -m autoflake --in-place --remove-unused-variables {} \;

lint:
	$(PYTHON) pylint $(PROJECT_HOME) > pylint.log

test:
	$(PYTHON) -m unittest

requirements:
	$(PYTHON) pip freeze > requirements.txt

testdeploy:
	docker stop $(DOCKER_CONTAINER)
	docker rm $(DOCKER_CONTAINER)
	docker rmi $(DOCKER_IMAGE);docker build -t $(DOCKER_IMAGE) .
	docker run --name $(DOCKER_CONTAINER) -d -p 8000:5000 $(DOCKER_IMAGE):latest

nest:
	cat example_input.json | $(PYTHON) nest.py currency country city 
