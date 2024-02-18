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
	@echo "===================================="
	$(POETRY) run black src tests
	$(POETRY) run ruff src tests --fix
	$(POETRY) run pylint src tests
	$(POETRY) run mypy src
	@echo "===================================="
	@echo "=> All checks succeeded"

unit-test:
	@echo "=> Running unit tests"
	@echo "===================================="
	$(POETRY) run pytest --cov=src

test-audit: unit-test
	@echo "=> Running test coverage report"
	@echo "===================================="
	$(POETRY) run coverage report --show-missing --fail-under=$(MIN_TEST_COVERAGE)

local-server:
	@echo "=> Starting local API server"
	@echo "===================================="
	$(POETRY) run uvicorn cofundable.api:app --reload

migration:
	@echo "=> Creating alembic migration script"
	@echo "===================================="
	$(POETRY) run alembic migration --autogenerate -m $(MESSAGE)
	@echo "===================================="
	@echo "=> Migration script created, check the alembic/versions sub-directory"

migrate-up:
	@echo "=> Migrating to the latest version of the database schema"
	@echo "===================================="
	$(POETRY) run alembic upgrade head
	@echo "===================================="
	@echo "=> Migration completed successfully"

migrate-down:
	@echo "=> Migrating to the previous version of the database schema"
	@echo "===================================="
	$(POETRY) run alembic downgrade -1
	@echo "===================================="
	@echo "=> Migration completed successfully"
