"""Create an ORM model for the cause table in the database."""

from typing import Optional

from sqlalchemy.orm import relationship

from cofundable.models.associations import cause_tag_table
from cofundable.models.base import Mapped, UUIDAuditBase
from cofundable.models.tag import Tag


class Cause(UUIDAuditBase):
    """Store information related to a cause."""

    name: Mapped[str]
    description: Mapped[Optional[str]]

    tags: Mapped[list[Tag]] = relationship(
        secondary=cause_tag_table,
        back_populates="causes",
    )
