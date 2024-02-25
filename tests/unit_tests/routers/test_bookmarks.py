"""Test the bookmark router in cofundable/routers/bookmarks.py."""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from cofundable.models import User
from tests.utils.test_data import ALICE


class TestListBookmarksForCurrentUser:
    """Test the GET /user/bookmarks/ endpoint."""

    ENDPOINT = "/user/bookmarks/"

    def test_return_correct_list_of_bookmarks(
        self,
        test_session: Session,
        test_client: TestClient,
    ):
        """The right set of bookmarks should be returned for the authed user."""
        # setup
        user = test_session.get(User, ALICE)
        assert user is not None
        # execution
        response = test_client.get(self.ENDPOINT)
        response_body = response.json()
        bookmarks = response_body.get("items")
        # validation
        assert response.status_code == 200
        assert bookmarks is not None
        assert len(bookmarks) == len(user.bookmarks)

    def test_response_should_be_paginated(self, test_client: TestClient):
        """The endpoint response should be paginated."""
        # execution
        response_body = test_client.get(self.ENDPOINT).json()
        # validation
        assert response_body.get("page") == 1  # page defaults to 1
        assert response_body.get("size") == 50  # size defaults to 50
        assert isinstance(response_body.get("items"), list)
        assert isinstance(response_body.get("links"), dict)


class TestBookmarkCauseForCurrentUser:
    """Test the PUT /user/bookmarks/{cause} endpoint."""

    def make_endpoint(self, cause: str) -> str:
        """Create the PUT endpoint to test."""
        return f"/user/bookmarks/{cause}"

    def test_return_status_code_200_and_body_if_successful(
        self,
        test_client: TestClient,
    ):
        """A successful response should return status code 201."""
        # execution
        response = test_client.put(self.make_endpoint("acme"))
        response_body = response.json()
        # validation
        assert response.status_code == 200
        assert response_body.get("created_at") is not None

    def test_multiple_endpoint_calls_return_same_response(
        self,
        test_client: TestClient,
    ):
        """Multiple calls should be idempotent."""
        # execution
        response1 = test_client.put(self.make_endpoint("acme"))
        response2 = test_client.put(self.make_endpoint("acme"))
        # validation
        assert response1.status_code == 200
        assert response1.status_code == 200
        assert response1.json() == response2.json()
