"""Create an ORM for the user table in the database."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import relationship

from cofundable.models.base import Mapped, UUIDAuditBase

if TYPE_CHECKING:
    from cofundable.models.bookmark import Bookmark
    from cofundable.models.cause import Cause


class User(UUIDAuditBase):
    """Store information related to a user."""

    username: Mapped[str]
    name: Mapped[str]
    bio: Mapped[str | None]

    bookmarks: Mapped[list[Bookmark]] = relationship(back_populates="user")

    # allows us to access bookmarked orgs directly
    bookmarked_causes: Mapped[list[Cause]] = relationship(
        secondary="bookmark",
        viewonly=True,
    )
