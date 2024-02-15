"""Populate the test database with test data."""

from sqlalchemy.orm import Session

from cofundable.models.cause import Cause
from cofundable.models.tag import Tag
from tests.utils import test_data as data


def populate_db(session: Session) -> None:
    """
    Populate the mock database with test data.

    Parameters
    ----------
    session: Session
        A SQLAlchemy session object passed to this function by the fixture

    """
    # init causes and tags
    causes = {id_: Cause(**fields) for id_, fields in data.CAUSES.items()}
    tags = {id_: Tag(**fields) for id_, fields in data.TAGS.items()}

    # associate tags with causes
    for cause_id, tag_ids in data.CAUSE_TAGS.items():
        cause = causes.get(cause_id)
        if not cause:
            continue
        for tag_id in tag_ids:
            tag = tags.get(tag_id)
            if tag:
                cause.tags.add(tag)

    # add records to session and then commit
    session.add_all(tags.values())
    session.add_all(causes.values())
    session.commit()
