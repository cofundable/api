"""Test the TransactionService class."""

import pytest
from sqlalchemy.orm import Session

from cofundable.models.account import Account
from cofundable.services.transactions import EntryType, transaction_service

from tests.utils import test_data

NAMESPACE = test_data.namespace


class TestQueryTransactionsByAccount:
    """Test the query_transactions_by_account() method."""

    def test_return_all_account_txn_by_default(self, test_session: Session):
        """All transactions associated with an account should be returned by default."""
        # setup
        account = test_session.get(Account, test_data.ACCOUNT_COFUNDABLE)
        assert account is not None
        txn_count = len(account.transactions)
        txn_ids = {txn.id for txn in account.transactions}
        # execution
        stmt = transaction_service.query_transactions_by_account(account)
        transactions = transaction_service.get_all(test_session, stmt)
        # validation
        assert len(transactions) == txn_count
        assert {txn.id for txn in transactions} == txn_ids

    @pytest.mark.parametrize(
        "entry_type",
        [EntryType.credit, EntryType.debit],
    )
    def test_filter_txn_by_entry_type(
        self,
        test_session: Session,
        entry_type: EntryType,
    ):
        """List of transactions should optionally be filtered by type."""
        # setup
        account = test_session.get(Account, test_data.ACCOUNT_ALICE)
        assert account is not None
        txn_count_all = len(account.transactions)
        # execution
        stmt = transaction_service.query_transactions_by_account(
            account=account,
            entry_type=entry_type,
        )
        transactions = transaction_service.get_all(test_session, stmt)
        # validation
        assert len(transactions) < txn_count_all
        for entry in transactions:
            assert entry.kind == entry_type
