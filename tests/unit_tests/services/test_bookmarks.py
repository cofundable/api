"""Test the cofundable.services.bookmarks module."""

from uuid import uuid5

import pytest
from sqlalchemy.orm import Session

from cofundable.models.bookmark import Bookmark
from cofundable.models.user import User
from cofundable.services.bookmarks import (
    bookmark_service,
    CauseHandleNotFoundError,
)
from cofundable.services.causes import cause_service
from tests.utils import test_data

NAMESPACE = test_data.namespace


class TestGetUserBookmarksPaginated:
    """Test the get_user_bookmarks_paginated() method."""

    def test_get_the_correct_results(self, test_session: Session):
        """The correct results should be returned for a given user."""
        # setup - get user
        alice_id = uuid5(NAMESPACE, "alice")
        alice = test_session.get(User, alice_id)
        assert alice is not None
        # execution
        stmt = bookmark_service.get_user_bookmarks_paginated(alice_id)
        bookmarks = test_session.execute(stmt).scalars().all()
        # validation
        assert len(alice.bookmarks) == len(bookmarks)
        assert alice.bookmarks == bookmarks


class TestBookmarkCauseForUser:
    """Test the bookmark_cause_for_user() method."""

    def test_bookmark_successfully_added(self, test_session: Session):
        """A new bookmark should be created and returned."""
        # setup - confirm user exists
        alice_id = uuid5(NAMESPACE, "alice")
        alice = test_session.get(User, alice_id)
        assert alice is not None
        # setup - confirm mutual-aid exists
        cause_handle = "mutual-aid"
        cause = cause_service.get_cause_by_handle(test_session, cause_handle)
        assert cause is not None
        # setup - confirm alice hasn't already bookmarked mutual-aid
        assert cause not in alice.bookmarked_causes
        # execution
        bookmark = bookmark_service.bookmark_cause_for_user(
            db=test_session,
            user_id=alice_id,
            cause_handle=cause_handle,
        )
        # validation
        assert isinstance(bookmark, Bookmark)
        assert bookmark.cause == cause
        assert bookmark.user == alice

    def test_raise_error_if_cause_does_not_exist(self, test_session: Session):
        """The CauseHandleNotFoundError should be raised if the cause doesn't exist."""
        # setup - get user_id
        user_id = uuid5(NAMESPACE, "alice")
        fake_handle = "fake"
        # validation - check that error is raised
        with pytest.raises(CauseHandleNotFoundError):
            bookmark_service.bookmark_cause_for_user(
                db=test_session,
                user_id=user_id,
                cause_handle=fake_handle,
            )
