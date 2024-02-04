import pytest
from fastapi.testclient import TestClient

from cofundable.api import app


@pytest.fixture(scope="session", name="client")
def mock_client():
    """Create a mock client to test the API."""
    return TestClient(app)
