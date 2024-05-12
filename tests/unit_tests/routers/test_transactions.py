"""Test the transaction router."""

from decimal import Decimal
from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from cofundable.models import Account
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

    def test_status_code_is_202(self, test_client: TestClient):
        """The status code should be 202."""
        # setup
        payload = {"to_account_id": test_data.ACCOUNT_AID.hex, "amount": 5.0}
        # execution
        response = test_client.post(self.ENDPOINT, json=payload)
        # validation
        if response.status_code != 202:
            print(response.json())
        assert response.status_code == 202

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

    def test_status_code_is_404_if_to_account_id_is_invalid(
        self,
        test_client: TestClient,
    ):
        """The status code should be 422 if the user's balance is too low."""
        # setup
        fake_account = uuid4()
        payload = {
            "to_account_id": fake_account.hex,
            "amount": 5,
        }
        # execution
        response = test_client.post(self.ENDPOINT, json=payload)
        # validation
        print(response.json())
        wanted = f"No account found with id: {fake_account.hex}"
        assert response.status_code == 404
        assert response.json()["detail"] == wanted

    def test_transfer_updates_account_balances(
        self,
        test_session: Session,
        test_client: TestClient,
        curr_user: User,
    ):
        """The balances of both the source and target accounts should be updated."""
        # setup - create the payload
        acme_account = test_session.get(Account, test_data.ACCOUNT_AID)
        assert acme_account is not None
        amount = 5.0
        payload = {"to_account_id": acme_account.id.hex, "amount": amount}
        # setup - get the current account balances for the source and target
        src_balance_old = curr_user.account.balance
        tgt_balance_old = acme_account.balance
        # execution
        response = test_client.post(self.ENDPOINT, json=payload)
        # validation
        assert response.status_code == 202
        src_balance_new = curr_user.account.balance
        tgt_balance_new = acme_account.balance
        assert src_balance_old - Decimal(amount) == src_balance_new
        assert tgt_balance_old + Decimal(amount) == tgt_balance_new
