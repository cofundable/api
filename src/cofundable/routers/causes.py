"""Route API requests related to Cofundable causes."""

from typing import Annotated, Sequence
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination.links import Page

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
    summary="Get a list of causes",
    response_model=Page[CauseResponseSchema],
)
def list_causes(db: Annotated[Session, Depends(get_db)]) -> Sequence[Cause]:
    """Fetch summary-level information about a list of causes."""
    return paginate(conn=db, query=cause_service.query_all())


@cause_router.post(
    "/",
    summary="Create a cause",
    response_model=CauseResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def post_cause(
    db: Annotated[Session, Depends(get_db)],
    payload: CauseRequestSchema,
) -> Cause:
    """Create a new cause."""
    return cause_service.create(db=db, data=payload)


@cause_router.get(
    "/{cause_id}",
    summary="Get cause details",
    response_model=CauseResponseSchema,
)
def get_cause_by_id(
    db: Annotated[Session, Depends(get_db)],
    cause_id: UUID,
) -> Cause:
    """Fetch the details for a specific cause using its id."""
    cause = cause_service.get(db=db, row_id=cause_id)
    if not cause:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cause not found",
        )
    return cause
