"""Test the cofundable.services.users module."""

from uuid import uuid5

from sqlalchemy import select
from sqlalchemy.orm import Session

from cofundable.models.bookmark import Bookmark
from cofundable.models.cause import Cause
from cofundable.models.user import User
from cofundable.schemas.user import UserUpdateSchema
from cofundable.services.users import user_service
from tests.utils import test_data

NAMESPACE = test_data.namespace


class TestGetUserByUsername:
    """Tests the get_user_by_handle() method."""

    def test_return_correct_user_if_they_exist(self, test_session: Session):
        """The correct user should be returned if they exist."""
        # setup - confirm the user exists
        handle = "alice"
        alice_id = uuid5(NAMESPACE, handle)
        alice = test_session.get(User, alice_id)
        assert alice is not None
        assert alice.handle == handle
        # execution
        user = user_service.get_user_by_handle(test_session, handle)
        assert user is not None
        assert user.handle == handle
        assert user == alice

    def test_return_none_if_user_does_not_exist(self, test_session: Session):
        """Return None if the handle doesn't match an existing user."""
        # setup
        handle = "fake"
        # execution
        result = user_service.get_user_by_handle(test_session, handle)
        # validation - check that the result is None
        assert result is None


class TestDelete:
    """Test the CauseCRUD.delete() method."""

    def test_delete_cascades_to_bookmarks_but_not_causes(
        self,
        test_session: Session,
    ):
        """Deleting a cause should delete associated bookmarks, but not users."""
        # set up - confirm alice exists
        alice_id = uuid5(NAMESPACE, "alice")
        assert test_session.get(User, alice_id) is not None
        # setup - confirm cause exists
        acme_id = uuid5(NAMESPACE, "acme")
        assert test_session.get(Cause, acme_id) is not None
        # set up - confirm bookmarks exist
        bookmark_query = select(Bookmark).where(Bookmark.user_id == alice_id)
        bookmarks_before = test_session.execute(bookmark_query).scalars().all()
        assert len(bookmarks_before) == 1
        # execution
        user_service.delete(test_session, row_id=alice_id)
        # validation - confirm user and bookmarks were deleted
        bookmarks_after = test_session.execute(bookmark_query).scalars().all()
        assert test_session.get(User, alice_id) is None
        assert len(bookmarks_after) == 0
        # validation - confirm cause was NOT deleted
        assert test_session.get(Cause, acme_id) is not None


class TestUpdate:
    """Tests the CauseCRUD.update() method."""

    def test_update_all_fields_successfully(self, test_session: Session):
        """Successfully update fields that support writes."""
        # setup
        alice = user_service.get(test_session, test_data.ALICE)
        assert alice is not None
        alice_old = dict(alice.__dict__)  # create a static copy of old values
        data = UserUpdateSchema(
            name="Alice Jones",
            handle="alice123",
            bio="This is a bio for alice",
        )
        # execution
        user_service.update(test_session, record=alice, update_data=data)
        # validation
        alice_new = dict(alice.__dict__)  # create a static copy of new values
        assert alice_new != alice_old
        for field, value in data.model_dump().items():
            assert alice_new[field] == value

    def test_skip_update_for_fields_that_are_unset(
        self,
        test_session: Session,
    ):
        """Fields that are unset in the update_data should be left as is."""
        # setup
        alice = user_service.get(test_session, test_data.ALICE)
        assert alice is not None
        alice_old = dict(alice.__dict__)  # create a static copy of old values
        data = UserUpdateSchema(bio="This is an updated bio")
        # execution
        user_service.update(test_session, record=alice, update_data=data)
        # validation
        alice_new = dict(alice.__dict__)  # create a static copy of new values
        assert alice_new != alice_old
        for field, value in data.model_dump().items():
            if value is None:
                assert alice_new[field] == alice_old[field]
            else:
                assert alice_new[field] == value
