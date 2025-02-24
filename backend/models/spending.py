from uuid import UUID
import datetime

from pydantic import BaseModel

from backend.models.currency import CurrencyResponse
from backend.models.category import CategoryResponse


class SpendingResponse(BaseModel):
    id: UUID
    amount: float
    description: str | None
    date: datetime.date
    currency: CurrencyResponse
    category: CategoryResponse

    class ConfigDict:
        from_attributes = True


class CreateSpending(BaseModel):
    amount: float
    date: datetime.date | None = None
    currency_id: UUID
    category_id: UUID
    description: str | None = None


class UpdateSpending(BaseModel):
    amount: float | None = None
    date: datetime.date | None = None
    description: str | None = None
    currency_id: UUID | None = None
    category_id: UUID | None = None
