"""Create an ORM model for the cause table in the database."""

from sqlalchemy.orm import relationship

from cofundable.models.associations import cause_tag_table
from cofundable.models.base import Mapped, UUIDAuditBase
from cofundable.models.bookmark import Bookmark
from cofundable.models.tag import Tag


class Cause(UUIDAuditBase):
    """Store information related to a cause."""

    name: Mapped[str]
    handle: Mapped[str]
    description: Mapped[str | None]

    tags: Mapped[set[Tag]] = relationship(
        secondary=cause_tag_table,
        back_populates="causes",
    )

    user_bookmarks: Mapped[list[Bookmark]] = relationship(
        back_populates="cause",
    )
