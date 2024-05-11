"""Test the transaction router."""

from fastapi.testclient import TestClient

from cofundable.models import User
from tests.utils import test_data


class TestListUserTransactions:
    """Test the GET /user/transactions/ endpoint."""

    ENDPOINT = "/user/transactions/"

    def test_status_code_is_200(self, test_client: TestClient):
        """The status code should be 200."""
        # execution
        response = test_client.get(self.ENDPOINT)
        # validation
        print(response.json()["items"][0])
        assert response.status_code == 200


class TestListCauseTransactions:
    """Test the GET /causes/{cause_id}/transactions/ endpoint."""

    def endpoint(self, cause_handle: str) -> str:
        """Make the endpoint path to test."""
        return f"/causes/{cause_handle}/transactions/"

    def test_status_code_is_200(self, test_client: TestClient):
        """The status code should be 200."""
        # execution
        cofundable = test_data.CAUSES[test_data.COFUNDABLE]
        endpoint = self.endpoint(cofundable["handle"])
        response = test_client.get(endpoint)
        # validation
        assert response.status_code == 200

    def test_status_code_is_404_when_given_invalid_cause_handle(
        self,
        test_client: TestClient,
    ):
        """The status code should be 200."""
        # execution
        endpoint = self.endpoint("fake")
        response = test_client.get(endpoint)
        # validation
        assert response.status_code == 404


class TestTransferShares:
    """Test the GET /causes/ endpoint."""

    ENDPOINT = "/user/transactions/transfer"

    def test_status_code_is_201(self, test_client: TestClient):
        """The status code should be 201."""
        # setup
        payload = {"to_account_id": test_data.ACCOUNT_AID.hex, "amount": 5.0}
        # execution
        response = test_client.post(self.ENDPOINT, json=payload)
        # validation
        if response.status_code != 201:
            print(response.json())
        assert response.status_code == 201

    def test_status_code_is_400_if_amount_exceeds_account_balance(
        self,
        test_client: TestClient,
        curr_user: User,
    ):
        """The status code should be 422 if the user's balance is too low."""
        # setup
        transfer_amount = 100
        assert curr_user.account.balance < transfer_amount
        payload = {
            "to_account_id": test_data.ACCOUNT_AID.hex,
            "amount": transfer_amount,
        }
        # execution
        response = test_client.post(self.ENDPOINT, json=payload)
        # validation
        print(response.json())
        assert response.status_code == 400
        assert "doesn't have enough" in response.json()["detail"]
