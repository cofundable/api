"""Test the causes_router in cofundable/routers/causes.py."""

from fastapi.testclient import TestClient


class TestGetCauses:
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
