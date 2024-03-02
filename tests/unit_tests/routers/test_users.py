"""Test the user router in cofundable/routers/users.py."""

from fastapi.testclient import TestClient


class TestGetCurrentLoggedInUser:
    """Test the GET /user/ endpoint."""

    ENDPOINT = "/user/"

    def test_status_code_200_when_user_is_logged_in(
        self,
        test_client: TestClient,
    ):
        """Status code should be 200 when the current user is logged in."""
        # execution
        response = test_client.get(self.ENDPOINT)
        # validation
        assert response.status_code == 200


class TestCreateUser:
    """Test the POST /users/ endpoint."""

    ENDPOINT = "/users/"

    def test_status_code_201_when_user_is_created(
        self,
        test_client: TestClient,
    ):
        """Status code should be 200 when the current user is logged in."""
        # setup
        data = {
            "name": "Test User",
            "bio": "Test bio",
            "handle": "testuser",
        }
        # execution
        response = test_client.post(self.ENDPOINT, json=data)
        # validation
        assert response.status_code == 201

    def test_status_code_422_when_required_field_is_missing(
        self,
        test_client: TestClient,
    ):
        """Status code should be 200 when the current user is logged in."""
        # setup
        data = {  # missing name
            "bio": "Test bio",
            "handle": "testuser",
        }
        # execution
        response = test_client.post(self.ENDPOINT, json=data)
        # validation
        assert response.status_code == 422
