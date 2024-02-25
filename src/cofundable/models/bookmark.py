"""Create an ORM for the bookmark table in the database."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import UUID, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from cofundable.models.base import Mapped, UUIDAuditBase, mapped_column

if TYPE_CHECKING:  # pragma: no cover
    from cofundable.models.cause import Cause
    from cofundable.models.user import User


class Bookmark(UUIDAuditBase):
    """Store information related to a user's bookmarks."""

    __table_args__ = (UniqueConstraint("user_id", "cause_id"),)

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id"),
        nullable=False,
    )
    cause_id: Mapped[UUID] = mapped_column(
        ForeignKey("cause.id"),
        nullable=False,
    )

    # associations between Bookmark -> User
    user: Mapped[User] = relationship(back_populates="bookmarks")

    # associations between Bookmark -> Cause
    cause: Mapped[Cause] = relationship(back_populates="user_bookmarks")
