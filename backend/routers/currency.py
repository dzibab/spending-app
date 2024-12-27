from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.db.session import get_db
from backend.db.models import Currency
from backend.models.currency import CurrencyCreate, CurrencyResponse


router = APIRouter(prefix="/currency", tags=["currency"])


@router.get("/", response_model=list[CurrencyResponse])
async def get_currencies(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Currency))
    currencies = result.scalars().all()
    if not currencies:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No currencies found")
    return currencies


@router.post("/", response_model=CurrencyResponse, status_code=status.HTTP_201_CREATED)
async def create_currency(currency: CurrencyCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Currency).where(Currency.name == currency.name))
    existing_currency = result.scalars().first()
    if existing_currency:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Currency already exists"
        )

    new_currency = Currency(name=currency.name.upper())
    db.add(new_currency)
    await db.commit()
    await db.refresh(new_currency)
    return new_currency


@router.delete("/{currency_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_currency(currency_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Currency).where(Currency.id == currency_id))
    currency = result.scalars().first()
    if not currency:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Currency not found")

    await db.delete(currency)
    await db.commit()
