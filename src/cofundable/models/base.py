"""Create base models that other models can inherit from."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import functions


class UUIDAuditBase(DeclarativeBase):
    """Base db model that includes id, created_at, and update_at."""

    id: Mapped[UUID] = mapped_column(primary_key=True)
    created_at = mapped_column(
        DateTime(timezone=True),
        default=functions.now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=functions.now,
        onupdate=functions.now,
    )
