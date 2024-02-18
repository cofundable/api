"""Routes API requests related to Cofundable causes."""

from typing import Annotated, Sequence

from fastapi import APIRouter, Depends
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
    summary="Search causes",
    response_model=Page[CauseResponseSchema],
)
def get_causes(db: Annotated[Session, Depends(get_db)]) -> Sequence[Cause]:
    """Get a list of causes."""
    return paginate(conn=db, query=cause_service.get_all_paginated())


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
