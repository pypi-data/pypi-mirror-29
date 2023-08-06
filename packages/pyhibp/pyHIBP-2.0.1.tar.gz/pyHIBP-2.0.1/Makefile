# Directories that might be created during testing
TESTING_DIRS := .tox .eggs .cache build dist htmlcov src/pyHIBP.egg-info

# Likewise for files
TESTING_FILES := .coverage .pipenv-made Pipfile.lock

build:
	pipenv run python setup.py sdist bdist_wheel

# Create a target to create a pipenv once, then we can reuse it.
.PHONY:create-pipenv
create-pipenv:
	@if [ ! -f .pipenv-made ]; then \
		pipenv install --dev; \
		pipenv install -e .; \
		touch .pipenv-made; \
	fi

.PHONY: clean
clean:
	find . -type f -name '*.py[co]' -delete

.PHONY: dist-clean
dist-clean: clean
	- pipenv --rm
	- rm $(TESTING_FILES)
	- rm -r $(TESTING_DIRS)

.PHONY: dev
dev: create-pipenv

.PHONY: test
test: create-pipenv
	pipenv run pytest

.PHONY: test-cov
test-cov: create-pipenv
	pipenv run pytest --cov=pyHIBP test/

.PHONY: check
check: create-pipenv
	pipenv run flake8

.PHONY: tox
tox: create-pipenv
	pipenv run tox
