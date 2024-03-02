"""Test the causes_router in cofundable/routers/causes.py."""

from uuid import UUID, uuid4

from fastapi.testclient import TestClient

from tests.utils import test_data


class TestListCauses:
    """Test the GET /causes/ endpoint."""

    ENDPOINT = "/causes/"

    def test_response_code_is_200(self, test_client: TestClient):
        """The status code should be 200."""
        # execution
        response = test_client.get(self.ENDPOINT)
        # validation
        print(response.json()["items"][0])
        assert response.status_code == 200

    def test_response_should_be_paginated(self, test_client: TestClient):
        """The endpoint response should be paginated."""
        # execution
        response_body = test_client.get(self.ENDPOINT).json()
        # validation
        assert response_body.get("page") == 1  # page defaults to 1
        assert response_body.get("size") == 50  # size defaults to 50
        assert isinstance(response_body.get("items"), list)
        assert isinstance(response_body.get("links"), dict)

    def test_change_item_count_with_pagination_params(
        self,
        test_client: TestClient,
    ):
        """The number of items returned should be influenced by size param."""
        # setup
        params = {"size": 1, "page": 1}
        # execution
        response_body = test_client.get(self.ENDPOINT, params=params).json()
        # validation
        assert len(response_body["items"]) == 1
        assert response_body["links"]["next"] is not None
        assert response_body["links"]["prev"] is None


class TestPostCause:
    """Test the POST /causes/ endpoint."""

    ENDPOINT = "/causes/"

    def test_return_status_code_201_if_successful(
        self,
        test_client: TestClient,
    ):
        """A successful response should return status code 201."""
        # setup
        payload = {
            "name": "Test cause",
            "description": "This is a test description.",
            "handle": "testcause",
            "tags": ["a", "b"],
        }
        # execution
        response = test_client.post(self.ENDPOINT, json=payload)
        response_body = response.json()
        # validation
        assert response.status_code == 201
        assert response_body["name"] == "Test cause"

    def test_return_status_code_422_if_missing_required_field(
        self,
        test_client: TestClient,
    ):
        """If a required field is missing, return status code 422."""
        # setup
        payload = {
            "name": "Test cause with missing handle",
            "tags": ["a", "b"],
        }
        # execution
        response = test_client.post(self.ENDPOINT, json=payload)
        # validation - check that status code is 422
        assert response.status_code == 422

    def test_create_cause_without_desc_or_tags(self, test_client: TestClient):
        """We should be able to create an org without tags or a description."""
        # setup
        payload = {
            "name": "Test cause with only required fields",
            "handle": "test-cause-only-required",
        }
        # execution
        response = test_client.post(self.ENDPOINT, json=payload)
        response_body = response.json()
        print(response_body)
        # validation - check that status code is 201 and fields are empty
        assert response.status_code == 201
        assert response_body["tags"] == []
        assert response_body["description"] is None


class TestGetCauseById:
    """Test the GET /causes/<cause_id> endpoint."""

    def endpoint(self, cause_id: UUID) -> str:
        """Make the endpoint path to test."""
        return f"/causes/{cause_id}"

    def test_return_correct_cause(self, test_client: TestClient):
        """The correct cause should be returned."""
        # setup
        acme_id = test_data.ACME
        endpoint = self.endpoint(acme_id)
        acme_data = test_data.CAUSES[acme_id]
        # execution
        response = test_client.get(endpoint)
        # validation
        assert response.status_code == 200
        assert response.json()["id"] == str(acme_id)
        assert response.json()["name"] == acme_data["name"]

    def test_return_404_if_id_has_no_match(self, test_client: TestClient):
        """Return 404 if id provided doesn't have a database match."""
        # setup - use an id that doesn't match an existing record
        endpoint = self.endpoint(uuid4())
        # execution
        response = test_client.get(endpoint)
        # validation - response code should be 404
        assert response.status_code == 404
        assert response.json() == {"detail": "Cause not found"}
