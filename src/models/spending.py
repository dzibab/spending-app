from uuid import UUID
from datetime import date

from pydantic import BaseModel


class Spending(BaseModel):
    id: UUID
    amount: float
    description: str
    date: date
    currency_id: UUID
    category_id: UUID

    class Config:
        from_attributes = True


class CreateSpending(BaseModel):
    amount: float
    date: date
    currency_id: UUID
    category_id: UUID
    description: str | None


class UpdateSpending(BaseModel):
    id: UUID
    amount: float | None
    date: date | None
    description: str | None
    currency_id: UUID | None
    category_id: UUID | None


class DeleteSpending(BaseModel):
    id: UUID
