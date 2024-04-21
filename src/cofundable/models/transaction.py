# pylint: disable=invalid-name
"""Create an ORM for the transaction table in the database."""

from __future__ import annotations

import uuid  # noqa: TCH003
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import UUID, ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, relationship

from cofundable.models.base import Mapped, UUIDAuditBase

if TYPE_CHECKING:
    from cofundable.models.account import Account


class EntryType(Enum):
    """Record entry as a credit or debit."""

    credit = "credit"
    debit = "debit"


class Transaction(UUIDAuditBase):
    """Store information related to a transaction in Cofundable."""

    __table_args__ = (UniqueConstraint("match_entry_id"),)

    # columns
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    amount: Mapped[float]
    kind: Mapped[EntryType]
    note: Mapped[str | None]
    account_id: Mapped[UUID] = mapped_column(
        ForeignKey("account.id"),
        nullable=False,
    )
    match_entry_id: Mapped[UUID] = mapped_column(
        ForeignKey("transaction.id"),
        nullable=True,
    )

    # relationships
    account: Mapped[Account] = relationship(back_populates="transactions")
    match_entry: Mapped[Transaction] = relationship(
        uselist=False,
        remote_side=[id],
        post_update=True,  # prevents circular dependency error
    )
