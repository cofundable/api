"""Test the cofundable.services.causes module."""

from uuid import UUID, uuid5

from sqlalchemy import select
from sqlalchemy.orm import Session

from cofundable.models.bookmark import Bookmark
from cofundable.models.cause import Cause
from cofundable.models.user import User
from cofundable.schemas.cause import CauseRequestSchema
from cofundable.services.causes import cause_service
from cofundable.services.tags import tag_service
from tests.utils import test_data

NAMESPACE = test_data.namespace


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


class TestGetCauseByHandle:
    """Tests the get_cause_by_handle() method."""

    def test_return_correct_cause_if_it_exists(self, test_session: Session):
        """The correct cause should be returned if it exists."""
        # setup - confirm the user exists
        handle = "acme"
        acme_id = uuid5(NAMESPACE, handle)
        acme = test_session.get(Cause, acme_id)
        assert acme is not None
        assert acme.handle == handle
        # execution
        cause = cause_service.get_cause_by_handle(test_session, handle)
        assert cause is not None
        assert cause.handle == handle
        assert cause == acme


class TestDelete:
    """Test the CauseCRUD.delete() method."""

    def test_delete_cascades_to_bookmarks_but_not_users(
        self,
        test_session: Session,
    ):
        """Deleting a cause should delete associated bookmarks, but not users."""
        # setup - confirm cause exists
        handle = "acme"
        acme_id = uuid5(NAMESPACE, handle)
        assert test_session.get(Cause, acme_id) is not None
        # set up - confirm bookmarks exist
        bookmark_query = select(Bookmark).where(Bookmark.cause_id == acme_id)
        bookmarks_before = test_session.execute(bookmark_query).scalars().all()
        assert len(bookmarks_before) > 1
        # set up - confirm alice exists
        alice_id = uuid5(NAMESPACE, "alice")
        assert test_session.get(User, alice_id) is not None
        # execution
        cause_service.delete(test_session, row_id=acme_id)
        # validation - confirm cause and bookmarks were deleted
        bookmarks_after = test_session.execute(bookmark_query).scalars().all()
        assert test_session.get(Cause, acme_id) is None
        assert len(bookmarks_after) == 0
        # validation - confirm alice was NOT deleted
        assert test_session.get(User, alice_id) is not None
