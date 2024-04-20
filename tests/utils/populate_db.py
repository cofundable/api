"""Populate the test database with test data."""

from sqlalchemy.orm import Session

from cofundable.models.base import UUIDAuditBase
from tests.utils import test_data as data


def create_records_and_add_to_session(
    model: type[UUIDAuditBase],
    records: dict,
    session: Session,
) -> dict[str, UUIDAuditBase]:
    """
    Create records with the data and model provided and add them to the session.

    Parameters
    ----------
    model: type[UUIDAuditBase]
        A subclass of UUIDAuditBase model to use to create the record
    records: list[TestRecord]
        A list of items that map the record id to the record's input data
    session:
        A SQLAlchemy session that will commit the resulting records to the db

    """
    record_map = {}
    for record_id, test_data in records.items():
        if "amount" in test_data:
            print(test_data)
        record = model(id=record_id, **test_data)
        record_map[record_id] = record
        session.add(record)
    return record_map


def populate_db(session: Session) -> None:
    """
    Populate the mock database with test data.

    Parameters
    ----------
    session: Session
        A SQLAlchemy session object passed to this function by the fixture

    """
    # populate UUID-based tables
    records = {}
    for table, test_data in data.UUID_TABLES.items():
        records[table] = create_records_and_add_to_session(
            session=session,
            model=test_data.model,
            records=test_data.records,
        )

    # associate tags with causes
    for cause_id, tag_ids in data.CAUSE_TAGS.items():
        cause = records["cause"][cause_id]
        for tag_id in tag_ids:
            tag = records["tag"][tag_id]
            cause.tags.add(tag)

    # commit the changes
    session.commit()
