# pylint: disable=C0103
"""Configure shared fixtures and pytest settings."""

from typing import Generator

import pytest
from dynaconf import Dynaconf
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from cofundable import config
from cofundable.api import app
from cofundable.dependencies import database, auth
from cofundable.models import User
from cofundable.services.users import user_service

from tests.utils.populate_db import populate_db
from tests.utils.test_data import ALICE


@pytest.fixture(scope="session", name="test_config")
def fixture_config():
    """Return the configuration settings for use in tests."""
    return config.settings.from_env("testing")


@pytest.fixture(scope="session", name="session")
def fixture_db(test_config: Dynaconf):
    """Create a connection to a test db with scope session."""
    # check that the testing configs are correctly set
    assert test_config.database_url == "sqlite:///mock.db"
    # connect to mock.db using the sqlalchemy engine
    engine = create_engine(
        url=test_config.database_url,
        pool_pre_ping=True,
        connect_args={"check_same_thread": False},
    )
    # initiate a db session using that connection
    test_session = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )
    with test_session() as session:
        database.init_test_db(session, testing=True)
        populate_db(session)
        yield session


@pytest.fixture(name="test_session")
def fixture_scoped_session(session: Session, monkeypatch: pytest.MonkeyPatch):
    """Create a scoped session that automatically rolls back after each test."""

    def flush_instead_of_commit() -> None:
        """Flush the transaction instead of committing it to allow rollback."""
        session.flush()
        session.expire_all()

    # replace commit() with flush() to enable rolling back test-specific changes
    monkeypatch.setattr(session, "commit", flush_instead_of_commit)
    # started a nested transaction then yield the session for use in a test
    session.begin_nested()
    yield session
    # roll back the transaction explicitly to undo the changes made in a test
    session.rollback()


@pytest.fixture(name="curr_user")
def fixture_current_user(test_session: Session) -> User:
    """Return a users as the current user."""
    user = user_service.get(test_session, ALICE)
    assert user is not None
    return user


@pytest.fixture(name="test_client")
def mock_client(test_session: Session, curr_user: User) -> TestClient:
    """Create a mock client to test the API."""

    def override_get_db() -> Generator[Session, None, None]:
        """Override the get_db() dependency to yield a test session."""
        yield test_session

    def override_get_current_user() -> User:
        """Override the get_current_user() dependency for authenticated endpoints."""
        return curr_user

    app.dependency_overrides[database.get_db] = override_get_db
    app.dependency_overrides[auth.get_current_user] = override_get_current_user
    return TestClient(app)
