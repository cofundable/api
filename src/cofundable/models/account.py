"""
Create an ORM for the account table in the database.

Accounts associate transactions with a given User or Cause, allowing each user
or cause to earn, spend, and pledge shares in Cofundable.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Numeric
from sqlalchemy.orm import relationship

from cofundable.models.base import Mapped, UUIDAuditBase, mapped_column

if TYPE_CHECKING:  # pragma: no cover
    from cofundable.models.cause import Cause
    from cofundable.models.user import User


class Account(UUIDAuditBase):
    """Manage transactions for a user or cause."""

    name: Mapped[str]
    balance: Mapped[Numeric] = mapped_column(Numeric)

    # Each account should have either a user or a cause but not both
    user: Mapped[User] = relationship(back_populates="account")
    cause: Mapped[Cause] = relationship(back_populates="account")
