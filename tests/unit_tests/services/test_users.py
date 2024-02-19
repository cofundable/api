"""Test the cofundable.services.users module."""

from uuid import uuid5

from sqlalchemy.orm import Session

from cofundable.models.user import User
from cofundable.services.users import user_service
from tests.utils import test_data


class TestGetUserByUsername:
    """Tests the get_user_by_username() method."""

    def test_return_correct_user_if_they_exist(self, test_session: Session):
        """The correct user should be returned if they exist."""
        # setup - confirm the user exists
        username = "alice"
        namespace = test_data.namespace
        alice_id = uuid5(namespace, username)
        alice = test_session.get(User, alice_id)
        assert alice is not None
        assert alice.username == username
        # execution
        user = user_service.get_user_by_username(test_session, username)
        assert user is not None
        assert user.username == username
        assert user == alice

    def test_return_none_if_user_does_not_exist(self, test_session: Session):
        """Return None if the username doesn't match an existing user."""
        # setup
        username = "fake"
        # execution
        result = user_service.get_user_by_username(test_session, username)
        # validation - check that the result is None
        assert result is None
