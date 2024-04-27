"""Handle business logic for accounts that store share balances in Cofundable."""

from decimal import Decimal

import sqlalchemy as sa
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
        # create and return transaction without committing
        return self.create(
            db=db,
            data=TransactionCreateSchema(
                amount=amount,
                kind=kind,
                account_id=account.id,
            ),
            defer_commit=True,
        )

    def query_transactions_by_account(
        self,
        account: Account,
        entry_type: EntryType | None = None,
    ) -> sa.Select:
        """Return a query that filters transactions by account_id."""
        # select transactions for a given account
        stmt = sa.select(Transaction)
        stmt = stmt.where(Transaction.account_id == account.id)
        if entry_type:
            stmt = stmt.where(Transaction.kind == entry_type)
        return stmt.order_by(sa.desc(Transaction.created_at))


transaction_service = TransactionService(model=Transaction)
