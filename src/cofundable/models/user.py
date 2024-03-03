"""Create an ORM for the user table in the database."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import UUID, ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, relationship

from cofundable.models.base import Mapped, UUIDAuditBase

if TYPE_CHECKING:  # pragma: no cover
    from cofundable.models.account import Account
    from cofundable.models.bookmark import Bookmark
    from cofundable.models.cause import Cause


class User(UUIDAuditBase):
    """Store information related to a user."""

    __table_args__ = (UniqueConstraint("account_id"),)

    handle: Mapped[str]
    name: Mapped[str]
    bio: Mapped[str | None]
    account_id: Mapped[UUID] = mapped_column(
        ForeignKey("account.id"),
        nullable=True,
    )

    # #########################################################
    # Relationships
    # #########################################################

    # Each user should only have one account
    account: Mapped[Account] = relationship(back_populates="user")

    bookmarks: Mapped[list[Bookmark]] = relationship(
        back_populates="user",
        cascade="delete",
    )

    # allows us to access bookmarked orgs directly
    bookmarked_causes: Mapped[list[Cause]] = relationship(
        secondary="bookmark",
        viewonly=True,
    )
