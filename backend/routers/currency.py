from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.db.session import get_db
from backend.db.models import Currency
from backend.models.currency import CurrencyCreate, CurrencyResponse

router = APIRouter(prefix="/currency", tags=["currency"])


async def get_currency_by_name(db: AsyncSession, name: str):
    result = await db.execute(select(Currency).where(Currency.name == name))
    return result.scalars().first()


async def get_currency_by_id(db: AsyncSession, currency_id: UUID):
    result = await db.execute(select(Currency).where(Currency.id == currency_id))
    return result.scalars().first()


@router.get("/", response_model=list[CurrencyResponse])
async def get_currencies(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Currency))
    currencies = result.scalars().all()
    if not currencies:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No currencies found")
    return [
        CurrencyResponse.model_validate(currency, from_attributes=True) for currency in currencies
    ]


@router.post("/", response_model=CurrencyResponse, status_code=status.HTTP_201_CREATED)
async def create_currency(currency: CurrencyCreate, db: AsyncSession = Depends(get_db)):
    existing_currency = await get_currency_by_name(db, currency.name)
    if existing_currency:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Currency already exists"
        )

    new_currency = Currency(name=currency.name.upper())
    db.add(new_currency)
    await db.commit()
    await db.refresh(new_currency)
    return CurrencyResponse.model_validate(new_currency, from_attributes=True)


@router.delete("/{currency_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_currency(currency_id: UUID, db: AsyncSession = Depends(get_db)):
    currency = await get_currency_by_id(db, currency_id)
    if not currency:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Currency not found")

    await db.delete(currency)
    await db.commit()
