"""Create association tables for many-to-many relationships."""

from sqlalchemy import Column, ForeignKey, Table

from cofundable.models.base import UUIDAuditBase

cause_tag_table = Table(
    "cause_tag",
    UUIDAuditBase.metadata,
    Column("cause_id", ForeignKey("cause.id"), primary_key=True),
    Column("tag_id", ForeignKey("tag.id"), primary_key=True),
)
