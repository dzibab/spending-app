from uuid import UUID
from datetime import date

from pydantic import BaseModel


class Spending(BaseModel):
    id: UUID
    amount: float
    description: str
    date: date
    currency: str
    category: str


class CreateSpending(Spending):
    amount: float
    currency: str
    category: str
    description: str | None


class UpdateSpending(Spending):
    id: UUID
    amount: float | None
    description: str | None
    currency: str | None
    category: str | None


class DeleteSpending(BaseModel):
    id: UUID
