POETRY ?= poetry run
MIN_TEST_COVERAGE ?= 80

#####################
# Build commands #
#####################

check-prereqs:
	@echo "=> Checking for pre-requisites"
	@if ! poetry --version; then echo "=> Poetry isn't installed" && exit 1; fi
	@echo "=> All pre-requisites satisfied"

install: check-prereqs
	@echo "=> Installing python dependencies"
	poetry install

local-server:
	@echo "=> Starting local API server"
	@echo "===================================="
	$(POETRY) uvicorn cofundable.api:app --reload

##########################
# Formatting and linting #
##########################

format: ## runs code formatting
	@echo "=> Running code formatting"
	@echo "============================="
	$(POETRY) black src tests
	$(POETRY) ruff --fix src tests
	@echo "============================="
	@echo "=> Code formatting complete"

format-check: ## runs code formatting checks
	@echo "=> Running code formatting checks"
	@echo "============================="
	$(POETRY) black --check src tests
	$(POETRY) ruff  --fix --exit-non-zero-on-fix src tests
	@echo "============================="
	@echo "=> All formatting checks succeeded"

lint: format-check
	@echo "============================="
	@echo "=> Running linters"
	@echo "============================="
	$(POETRY) pylint src tests
	$(POETRY) mypy src
	@echo "============================="
	@echo "=> All linters succeeded"

#################
# Test commands #
#################

unit-test:
	@echo "=> Running unit tests"
	@echo "===================================="
	$(POETRY) pytest --cov=src

test-audit: unit-test
	@echo "=> Running test coverage report"
	@echo "===================================="
	$(POETRY) coverage report --show-missing --fail-under=$(MIN_TEST_COVERAGE)

#####################
# Database commands #
#####################

migration:
ifdef message
	@echo "=> Creating alembic migration script"
	@echo "===================================="
	$(POETRY) alembic revision --autogenerate -m "$(message)"
	@echo "===================================="
	@echo "=> Migration script created, check the alembic/versions sub-directory"
else
	@echo "Please pass a message for the migration script, for example:"
	@echo "make migration message='<Migration message>'"
endif

migrate-check:
	@echo "=> Checking if DB schema needs to be updated"
	@echo "===================================="
	$(POETRY) alembic check
	@echo "===================================="
	@echo "=> DB schema is up to date"

migrate-up:
	@echo "=> Migrating to the latest version of the database schema"
	@echo "===================================="
	$(POETRY) alembic upgrade head
	@echo "===================================="
	@echo "=> Migration completed successfully"

migrate-down:
	@echo "=> Migrating to the previous version of the database schema"
	@echo "===================================="
	$(POETRY) alembic downgrade -1
	@echo "===================================="
	@echo "=> Migration completed successfully"
