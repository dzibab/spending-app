from datetime import datetime

from pydantic import BaseModel


class SpendingCreate(BaseModel):
    description: str
    amount: float
    date: datetime
    currency: str
    category: str
