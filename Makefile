POETRY ?= poetry
MIN_TEST_COVERAGE ?= 80

check-prereqs:
	@echo "=> Checking for pre-requisites"
	@if ! $(POETRY) --version; then echo "=> Poetry isn't installed"; fi
	@echo "=> All pre-requisites satisfied"

install: check-prereqs
	@echo "=> Installing python dependencies"
	$(POETRY) install

lint:
	@echo "=> Running code quality checks"
	@echo "============================="
	$(POETRY) run black src tests
	$(POETRY) run ruff src tests --fix
	$(POETRY) run pylint src tests
	$(POETRY) run mypy src
	@echo "============================="
	@echo "=> All checks succeeded"

unit-test:
	@echo "=> Running unit tests"
	@echo "============================="
	$(POETRY) run pytest --cov=src

test-audit: unit-test
	@echo "=> Running test coverage report"
	@echo "============================="
	$(POETRY) run coverage report --show-missing --fail-under=$(MIN_TEST_COVERAGE)

local-server:
	@echo "=> Starting local API server"
	@echo "============================="
	$(POETRY) run uvicorn cofundable.api:app --reload
