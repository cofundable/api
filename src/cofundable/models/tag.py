"""Create an ORM for the tag table in the database."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import relationship

from cofundable.models.associations import cause_tag_table
from cofundable.models.base import Mapped, UUIDAuditBase

if TYPE_CHECKING:  # pragma: no cover
    from cofundable.models.cause import Cause


class Tag(UUIDAuditBase):
    """Store information related to a cause."""

    name: Mapped[str]
    description: Mapped[str | None]

    causes: Mapped[list[Cause]] = relationship(
        secondary=cause_tag_table,
        back_populates="tags",
    )
