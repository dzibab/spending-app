from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class SpendingCreate(BaseModel):
    description: str
    amount: float
    date: datetime
    currency: str
    category: str


class SpendingUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[float] = None
    date: Optional[datetime] = None
    currency: Optional[str] = None
    category: Optional[str] = None
