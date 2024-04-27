"""Test the cofundable.services.accounts module."""

from decimal import Decimal

from sqlalchemy.orm import Session

from cofundable.models.account import Account
from cofundable.services.accounts import account_service

from tests.utils import test_data

NAMESPACE = test_data.namespace


class TestTransferShares:
    """Test the AccountCRUD.transfer_shares() method."""

    def test_transaction_added_to_accounts(self, test_session: Session):
        """New transactions should appear in the transaction list for both accounts."""
        # setup
        source = test_session.get(Account, test_data.ACCOUNT_ACME)
        target = test_session.get(Account, test_data.ACCOUNT_ALICE)
        assert source is not None
        assert target is not None
        source_txn_count_old = len(source.transactions)
        target_txn_count_old = len(target.transactions)
        # execution
        debit, credit = account_service.transfer_shares(
            test_session,
            amount=5.0,
            from_account=source,
            to_account=target,
        )
        # validation - confirm transaction lists are longer
        assert len(source.transactions) > source_txn_count_old
        assert len(target.transactions) > target_txn_count_old
        # validation - confirm credit and debit are assigned to the right accounts
        assert debit.account == source
        assert credit.account == target

    def test_transactions_matched_to_each_other(self, test_session: Session):
        """New transactions should appear in the transaction list for both accounts."""
        # setup
        source = test_session.get(Account, test_data.ACCOUNT_ACME)
        target = test_session.get(Account, test_data.ACCOUNT_ALICE)
        assert source is not None
        assert target is not None
        # execution
        debit, credit = account_service.transfer_shares(
            test_session,
            amount=5.0,
            from_account=source,
            to_account=target,
        )
        # validation - confirm credit and debit are assigned to the right accounts
        assert debit.match_entry == credit
        assert credit.match_entry == debit

    def test_account_balances_updated(self, test_session: Session):
        """Transaction should appear in the transaction list for the target account."""
        # setup
        source = test_session.get(Account, test_data.ACCOUNT_ACME)
        target = test_session.get(Account, test_data.ACCOUNT_ALICE)
        assert source is not None
        assert target is not None
        source_balance_old = source.balance
        target_balance_old = target.balance
        # execution
        amount = Decimal(5.0)
        account_service.transfer_shares(
            test_session,
            amount=amount,
            from_account=source,
            to_account=target,
        )
        # validation - confirm balances were adjusted correctly
        assert source.balance == source_balance_old - amount
        assert target.balance == target_balance_old + amount
