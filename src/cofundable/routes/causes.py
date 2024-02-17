"""Routes API requests related to Cofundable causes."""

from typing import Annotated, Sequence

from fastapi import APIRouter, Depends

from cofundable.dependencies.database import Session, get_db
from cofundable.schemas.cause import CauseRequestSchema, CauseResponseSchema
from cofundable.services.causes import Cause, cause_service

cause_router = APIRouter(
    prefix="/causes",
    tags=["causes"],
    responses={404: {"description": "Not found"}},
)


@cause_router.get(
    "/",
    summary="Search causes",
    response_model=list[CauseResponseSchema],
)
def search_causes(db: Annotated[Session, Depends(get_db)]) -> Sequence[Cause]:
    """Get a list of causes."""
    return cause_service.get_all(db=db)


@cause_router.post(
    "/",
    summary="Create a cause",
    response_model=CauseResponseSchema,
)
def post_cause(
    db: Annotated[Session, Depends(get_db)],
    payload: CauseRequestSchema,
) -> Cause:
    """Create a new cause."""
    return cause_service.create(db=db, data=payload)
