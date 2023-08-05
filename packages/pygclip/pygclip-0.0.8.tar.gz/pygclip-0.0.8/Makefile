.PHONY: all clean install-dev lint test coverage cov tox audit build upload

all: test

clean:
	rm -rf build/
	rm -rf dist/
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

install-dev:
	pip install --quiet --editable .[dev]

lint: clean
	python setup.py lint

test: clean install-dev
	python setup.py test

coverage: clean install-dev
	coverage run -m pytest
	coverage report
	coverage html

cov: coverage

tox: clean install-dev
	tox

audit:
	python setup.py audit

build: clean
	python setup.py check
	python setup.py sdist
	python setup.py bdist_wheel

upload: clean
	python setup.py sdist upload
	python setup.py bdist_wheel upload
