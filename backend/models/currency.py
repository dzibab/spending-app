from uuid import UUID

from pydantic import BaseModel, Field


class CurrencyBase(BaseModel):
    name: str = Field(min_length=3, max_length=3)


class CurrencyCreate(CurrencyBase):
    pass


class CurrencyResponse(CurrencyBase):
    id: UUID

    class ConfigDict:
        from_attributes = True
