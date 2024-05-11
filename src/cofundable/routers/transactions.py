"""Route API requests related to transactions."""

from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination.links import Page
from sqlalchemy.orm import Session

from cofundable.dependencies.auth import get_current_user
from cofundable.dependencies.database import get_db
from cofundable.models.transaction import Transaction
from cofundable.models.user import User
from cofundable.schemas.transaction import (
    TransactionSchema,
    TransferSharesBodySchema,
)
from cofundable.services.causes import cause_service
from cofundable.services.transactions import transaction_service

transaction_router = APIRouter(
    tags=["transactions"],
    responses={404: {"description": "Not found"}},
)


@transaction_router.post(
    "/user/transactions/transfer",
    summary="Transfer shares from the current user",
    status_code=status.HTTP_201_CREATED,
)
def transfer_shares_for_current_user(
    curr_user: Annotated[User, Depends(get_current_user)],
    data: TransferSharesBodySchema,
) -> dict:
    """Transfer shares from the currently authenticated user to another account."""
    if curr_user.account.balance < data.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current user doesn't have enough shares to transfer that amount",
        )
    return data.model_dump()


@transaction_router.get(
    "/user/transactions",
    summary="List transactions for the current user",
    status_code=status.HTTP_200_OK,
    response_model=Page[TransactionSchema],
)
def list_user_transactions(
    db: Annotated[Session, Depends(get_db)],
    curr_user: Annotated[User, Depends(get_current_user)],
) -> Sequence[Transaction]:
    """List the transactions for the current user."""
    query = transaction_service.query_transactions_by_account(
        account=curr_user.account,
    )
    return paginate(conn=db, query=query)


@transaction_router.get(
    "/causes/{cause_handle}/transactions",
    summary="List transactions for a given cause",
    status_code=status.HTTP_200_OK,
    response_model=Page[TransactionSchema],
)
def list_cause_transactions(
    db: Annotated[Session, Depends(get_db)],
    cause_handle: str,
) -> Sequence[Transaction]:
    """List the transactions for the current user."""
    cause = cause_service.get_cause_by_handle(db, handle=cause_handle)
    if not cause:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cause not found",
        )
    query = transaction_service.query_transactions_by_account(
        account=cause.account,
    )
    return paginate(conn=db, query=query)
