from uuid import UUID

from pydantic import BaseModel


class CurrencyBase(BaseModel):
    name: str


class CurrencyCreate(CurrencyBase):
    pass


class CurrencyResponse(CurrencyBase):
    id: UUID

    class Config:
        from_attributes = True
