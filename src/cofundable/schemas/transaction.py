"""Declare schemas for transactions between accounts."""

from uuid import UUID

from pydantic import BaseModel

from cofundable.models.transaction import EntryType
from cofundable.schemas.account import AccountSchema


class TransactionSchema(BaseModel):
    """Base schema for a transaction, with common fields."""

    amount: int | float
    kind: EntryType
    note: str | None = None


class TransactionCreateSchema(TransactionSchema):
    """Schema used create a transaction."""

    account_id: UUID


class TransactionDumpSchema(TransactionSchema):
    """Schema used to serialize a transaction."""

    account: AccountSchema
    match_entry_id: UUID
