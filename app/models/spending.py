from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field


class SpendingBase(BaseModel):
    description: str = Field(..., description="A brief description of the spending.")
    amount: float = Field(..., description="The amount spent.")
    date: datetime = Field(..., description="The date and time when the spending occurred.")
    currency: str = Field(..., description="The currency in which the spending was made (e.g., USD, EUR).")
    category: str = Field(..., description="The category of the spending (e.g., Food, Entertainment).")

    model_config = {
        "from_attributes": True,
    }


class SpendingCreate(SpendingBase):
    pass


class SpendingUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[float] = None
    date: Optional[datetime] = None
    currency: Optional[str] = None
    category: Optional[str] = None


class Spending(SpendingBase):
    id: int  # Add the ID field to the response model
