WATCH_EVENTS=modify,close_write,moved_to,create

.PHONY: watch docs

init:  ## setup environment
	pip install pipenv
	pipenv install --dev

help:
	@for f in $(MAKEFILE_LIST) ; do \
		echo "$$f:" ; \
		grep -E '^[a-zA-Z_-%]+:.*?## .*$$' $$f | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}' ; \
	done ; \

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build:  ## remove build artifacts
	rm -rf build/ dist/ .eggs/
	rm -rf '*.egg-info'
	rm -rf '*.egg'

clean-pyc:  ## remove Python file artifacts
	find -name '*.pyc' -delete
	find -name '*.pyo' -delete
	find -name '*~' -delete
	find -name '__pycache__' -delete

clean-test:  ## remove test and coverage artifacts
	rm -rf .tox/ .coverage htmlcov/

lint:  ## run pre-commit hooks on all files
	pipenv run pre-commit run --files $$(git ls-files)

coverage: ## check code coverage quickly with the default Python
	pipenv run py.test \
		--cov-report html \
		--cov-report term \
		--cov-report term-missing \
		--cov=rest_witchcraft tests

test:  ## run tests
	pipenv run py.test tests

check:  ## run all tests
	tox

history:  ## generate HISTORY.rst
	pipenv run gitchangelog > HISTORY.rst

docs:  ## generate docs
	$(MAKE) -C docs html

version:
	@python setup.py --version

tag:  ## tags branch
	git tag -a $$(python setup.py --version) -m $$(python setup.py --version)

release: dist  ## package and upload a release
	twine upload dist/*

dist: clean  ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

watch:  ## watch file changes to run a command, e.g. make watch test
	@if ! type "inotifywait" > /dev/null; then \
		echo "Please install inotify-tools" ; \
	fi; \
	echo "Watching $(pwd) to run: $(WATCH_ARGS)" ; \
	while true; do \
		make $(WATCH_ARGS) ; \
		inotifywait -e $(WATCH_EVENTS) -r --exclude '.*(git|~)' . ; \
	done \

# If the first argument is "watch"...
ifeq (watch,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "watch"
  WATCH_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(WATCH_ARGS):;@:)
endif
