"""Test the cofundable.services.users module."""

from uuid import uuid5

from sqlalchemy.orm import Session

from cofundable.models.user import User
from cofundable.services.users import user_service
from tests.utils import test_data


class TestGetUserByUsername:
    """Tests the get_user_by_handle() method."""

    def test_return_correct_user_if_they_exist(self, test_session: Session):
        """The correct user should be returned if they exist."""
        # setup - confirm the user exists
        handle = "alice"
        namespace = test_data.namespace
        alice_id = uuid5(namespace, handle)
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
