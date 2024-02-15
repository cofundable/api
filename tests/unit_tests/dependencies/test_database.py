"""Test the database connection."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from cofundable.models.cause import Cause


def test_mock_db_initialized_correctly(test_session: Session):
    """The mock database for testing should be created and populated correctly."""
    # setup
    cause_name = "Acme"
    statement = select(Cause).where(Cause.name == cause_name)
    # execution
    cause = test_session.execute(statement).scalar()
    # validation
    assert cause is not None
    assert cause.name == "Acme"
    assert len(cause.tags) == 2
