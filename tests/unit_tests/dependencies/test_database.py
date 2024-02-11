"""Test the database connection."""

from sqlalchemy.orm import Session


def test_mock_db_initialized_correctly(test_session: Session):
    """The mock database for testing should be initialized correctly."""
    print(test_session.info)
    assert 0
