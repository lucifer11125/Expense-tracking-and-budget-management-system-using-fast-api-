from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserAuth(BaseModel):
    """Schema that is used for user input during signup or login."""
    username: str = Field(min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "harsh",
                "email": "harsh@example.com",
                "password": "secret123"
            }
        }
    )


class UserOut(BaseModel):
    """"Schema that defines what is sent back to the client."""
    id: str
    username: str 
    email: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "2f8c0c88-7e18-42f3-b721-2d5d6e6c4fd2",
                "username": "harsh",
                "email": "harsh@example.com"
            }
        }
    )


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "access-token-value",
                "refresh_token": "refresh-token-value",
                "token_type": "bearer"
            }
        }
    )


class ExpenseCreate(BaseModel):
    title: str = Field(min_length=2, max_length=80)
    amount: float = Field(gt=0)
    category: str = Field(min_length=2, max_length=40)
    spent_on: date
    note: str | None = Field(default=None, max_length=200)


class ExpenseUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=80)
    amount: float | None = Field(default=None, gt=0)
    category: str | None = Field(default=None, min_length=2, max_length=40)
    spent_on: date | None = None
    note: str | None = Field(default=None, max_length=200)


class ExpenseOut(ExpenseCreate):
    id: str
    user_id: str

    model_config = ConfigDict(from_attributes=True)


class BudgetCreate(BaseModel):
    category: str = Field(min_length=2, max_length=40)
    limit_amount: float = Field(gt=0)
    month: str = Field(pattern=r"^\d{4}-\d{2}$", examples=["2026-06"])


class BudgetUpdate(BaseModel):
    category: str | None = Field(default=None, min_length=2, max_length=40)
    limit_amount: float | None = Field(default=None, gt=0)
    month: str | None = Field(default=None, pattern=r"^\d{4}-\d{2}$")


class BudgetOut(BudgetCreate):
    id: str
    user_id: str

    model_config = ConfigDict(from_attributes=True)


class BudgetStatus(BaseModel):
    budget_id: str
    category: str
    month: str
    limit_amount: float
    spent: float
    remaining: float
    status: Literal["within_budget", "over_budget"]


class SummaryOut(BaseModel):
    total_spent: float
    expenses_count: int
    budgets: list[BudgetStatus]
