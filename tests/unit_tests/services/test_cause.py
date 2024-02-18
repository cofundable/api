"""Test the cofundable.services.causes module."""

from uuid import UUID

from sqlalchemy.orm import Session

from cofundable.models.cause import Cause
from cofundable.schemas.cause import CauseRequestSchema
from cofundable.services.causes import cause_service
from cofundable.services.tags import tag_service


class TestCreate:
    """Test the CauseCRUD.create() method."""

    def test_successfully_create_new_cause(self, test_session: Session):
        """A new cause should be created and returned."""
        # setup
        cause_data = CauseRequestSchema(
            name="Test Org",
            description="This is a test org",
            handle="testorg",
            tags=["a", "b", "c"],
        )
        # execution
        cause = cause_service.create(test_session, data=cause_data)
        # validation
        assert isinstance(cause, Cause)
        assert isinstance(cause.id, UUID)
        assert cause.created_at is not None
        assert cause.updated_at is not None
        assert cause.tags != set()

    def test_create_cause_with_existing_tags(self, test_session: Session):
        """No new tags should be created if the tags already exist."""
        # setup
        tags = ["a", "b", "c"]
        cause_data = CauseRequestSchema(
            name="Test Org",
            description="This is a test org",
            handle="testorg",
            tags=tags,
        )
        tags_old = tag_service.get_all(test_session)
        assert set(tags) == {tag.name for tag in tags_old}
        # execution
        cause = cause_service.create(test_session, data=cause_data)
        tags_new = tag_service.get_all(test_session)
        # validation - check that no new tags were created
        assert len(tags_old) == len(tags_new)
        assert tags_old == tags_new
        assert {tag.name for tag in cause.tags} == set(tags)
