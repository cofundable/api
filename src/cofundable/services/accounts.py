"""Handle business logic for accounts that store share balances in Cofundable."""

from decimal import Decimal

from sqlalchemy.orm import Session

from cofundable.models.account import Account
from cofundable.models.transaction import Transaction
from cofundable.schemas.account import AccountSchema
from cofundable.schemas.transaction import EntryType
from cofundable.services.base import CRUDBase
from cofundable.services.transactions import transaction_service


class AccountCRUD(CRUDBase[Account, AccountSchema, AccountSchema]):
    """Manage CRUD operations for the Cause model."""

    def transfer_shares(
        self,
        db: Session,
        amount: float | Decimal,
        from_account: Account,
        to_account: Account,
    ) -> tuple[Transaction, Transaction]:
        """Record matching transactions that transfer shares from account to another."""
        # create a matching credit and debit transactions
        debit = transaction_service.record_transaction(
            db=db,
            account=from_account,
            kind=EntryType.debit,
            amount=amount,
        )
        credit = transaction_service.record_transaction(
            db=db,
            account=to_account,
            kind=EntryType.credit,
            amount=amount,
        )
        debit.match_entry = credit
        credit.match_entry = debit
        # commit the transactions
        db.add_all([credit, debit])
        db.commit()
        return (debit, credit)


account_service = AccountCRUD(model=Account)
