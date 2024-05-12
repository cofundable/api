"""Declare schemas for accounts that store balances for users and causes."""

from pydantic import BaseModel


class AccountSchema(BaseModel):
    """Base schema for an account, with common fields."""

    name: str
    balance: int | float
