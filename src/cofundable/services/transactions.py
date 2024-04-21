"""Handle business logic for accounts that store share balances in Cofundable."""

from cofundable.models.transaction import Transaction
from cofundable.schemas.transaction import TransactionCreateSchema
from cofundable.services.base import InsertOnlyBase


class TransactionService(InsertOnlyBase[Transaction, TransactionCreateSchema]):
    """Manage CRUD operations for the Cause model."""


transaction_service = TransactionService(model=Transaction)
