"""Create an ORM for the bookmark table in the database."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import relationship

from cofundable.models.base import Mapped, UUIDAuditBase, mapped_column

if TYPE_CHECKING:
    from cofundable.models.cause import Cause
    from cofundable.models.user import User


class Bookmark(UUIDAuditBase):
    """Store information related to a user's bookmarks."""

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id"),
        primary_key=True,
    )
    cause_id: Mapped[str] = mapped_column(
        ForeignKey("cause.id"),
        primary_key=True,
    )

    # associations between Bookmark -> User
    user: Mapped[User] = relationship(back_populates="bookmarks")

    # associations between Bookmark -> Cause
    cause: Mapped[Cause] = relationship(back_populates="user_bookmarks")
