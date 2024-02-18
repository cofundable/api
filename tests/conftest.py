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
from cofundable.dependencies import database

from tests.utils.populate_db import populate_db


@pytest.fixture(scope="session", name="test_config")
def fixture_config():
    """Return the configuration settings for use in tests."""
    return config.settings.from_env("testing")


@pytest.fixture(name="test_session")
def fixture_session(test_config: Dynaconf):
    """Create a local database for unit testing."""
    # check that the testing configs are correctly set
    assert test_config.database_url == "sqlite:///mock.db"
    # connect to mock.db using the sqlalchemy engine
    engine = create_engine(
        url=test_config.database_url,
        pool_pre_ping=True,
        connect_args={"check_same_thread": False},
    )
    # initiate a db session using that connection
    TestSession = sessionmaker(  # noqa: N806
        autocommit=False,
        autoflush=False,
        bind=engine,
    )
    # yield that session after dropping and recreating the tables in the db
    with TestSession() as session:
        database.init_test_db(session, testing=True)
        populate_db(session)
        yield session


@pytest.fixture(name="test_client")
def mock_client(test_session: Session):
    """Create a mock client to test the API."""

    def override_get_db() -> Generator[Session, None, None]:
        """Override the get_db() dependency to yield a test session."""
        yield test_session

    app.dependency_overrides[database.get_db] = override_get_db
    return TestClient(app)
