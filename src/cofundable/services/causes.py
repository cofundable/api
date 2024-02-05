"""Handle business logic related to Cofundable causes."""

from datetime import UTC, datetime
from uuid import uuid4

from cofundable.schemas.cause import CauseRequestSchema, CauseResponseSchema


def create_cause(data: CauseRequestSchema) -> CauseResponseSchema:
    """Create a new cause and return the resulting record."""
    now = datetime.now(UTC)
    return CauseResponseSchema(
        **data.model_dump(),
        id=uuid4(),
        updated_at=now,
        created_at=now,
    )


def list_causes() -> list[CauseResponseSchema]:
    """Return a list of causes, optionally filtered by a set of fields."""
    now = datetime.now(UTC)
    return [
        CauseResponseSchema(
            id=uuid4(),
            created_at=now,
            updated_at=now,
            name="Acme",
            description="Test description",
            handle="acme",
        ),
    ]
