"""Handle business logic for accounts that store share balances in Cofundable."""

from decimal import Decimal

from sqlalchemy.orm import Session

from cofundable.models.account import Account
from cofundable.models.transaction import Transaction
from cofundable.schemas.transaction import EntryType, TransactionCreateSchema
from cofundable.services.base import InsertOnlyBase


class TransactionService(InsertOnlyBase[Transaction, TransactionCreateSchema]):
    """Manage CRUD operations for the Cause model."""

    def record_transaction(
        self,
        db: Session,
        account: Account,
        kind: EntryType,
        amount: float | Decimal,
    ) -> Transaction:
        """Record a transaction and update the associated account balance."""
        # update the account balance
        if kind == EntryType.debit:
            account.balance -= Decimal(amount)
        else:
            account.balance += Decimal(amount)
        db.add(account)
        return self.create(
            db=db,
            data=TransactionCreateSchema(
                amount=amount,
                kind=kind,
                account_id=account.id,
            ),
            defer_commit=True,
        )


transaction_service = TransactionService(model=Transaction)
