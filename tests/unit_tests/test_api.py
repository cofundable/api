from fastapi.testclient import TestClient


class TestHealthCheck:
    """Test the /health-check endpoint."""

    ENDPOINT = "/health-check"

    def test_status_code_should_be_200(self, client: TestClient):
        """The response status code should be 200."""
        response = client.get(self.ENDPOINT)
        assert response.status_code == 200

    def test_response_status_is_ok(self, client: TestClient):
        """The response json should contain a status key whose value is 'ok'."""
        response = client.get(self.ENDPOINT)
        assert response.json()["status"] == "ok"


class TestRoot:
    """Test the root `/` endpoint."""

    ENDPOINT = "/"

    def test_status_code_should_be_200(self, client: TestClient):
        """The response status code should be 200."""
        response = client.get(self.ENDPOINT)
        assert response.status_code == 200

    def test_response_contains_docs_endpoint(self, client: TestClient):
        """The response message should contain the path to `/docs`."""
        response = client.get(self.ENDPOINT)
        assert "/docs" in response.json()["message"]
