"""Create an ORM model for the cause table in the database."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import UUID, ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, relationship

from cofundable.models.associations import cause_tag_table
from cofundable.models.base import Mapped, UUIDAuditBase

if TYPE_CHECKING:  # pragma: no cover
    from cofundable.models.account import Account
    from cofundable.models.bookmark import Bookmark
    from cofundable.models.tag import Tag


class Cause(UUIDAuditBase):
    """Store information related to a cause."""

    __table_args__ = (UniqueConstraint("account_id"),)

    name: Mapped[str]
    handle: Mapped[str]
    description: Mapped[str | None]
    account_id: Mapped[UUID] = mapped_column(
        ForeignKey("account.id"),
        nullable=False,
    )

    # each cause should only have one account
    account: Mapped[Account] = relationship(back_populates="cause")

    # return associated tags as a set instead of a list
    tags: Mapped[set[Tag]] = relationship(
        secondary=cause_tag_table,
        back_populates="causes",
        cascade="save-update",
    )

    # return list of bookmarks for a given cause
    user_bookmarks: Mapped[list[Bookmark]] = relationship(
        back_populates="cause",
        cascade="delete",
    )
