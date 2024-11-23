from uuid import UUID
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound

from backend.db.models import Spending as SpendingDB, Currency as CurrencyDB, Category as CategoryDB
from backend.db.session import get_db
from backend.models.spending import CreateSpending, UpdateSpending, Spending


router = APIRouter(prefix="/spending", tags=["spending"])


@router.get("/", response_model=list[Spending])
async def get_spendings(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SpendingDB))
    spendings = result.scalars().all()
    return spendings


@router.get("/{spending_id:uuid}", response_model=Spending)
async def get_spending(spending_id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(SpendingDB).where(SpendingDB.id == spending_id))
        spending = result.scalar_one()
        return spending
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Spending not found")


@router.get("/current-month", response_model=list[Spending])
async def get_spendings_current_month(db: AsyncSession = Depends(get_db)):
    today = date.today()
    start_of_month = today.replace(day=1)

    try:
        result = await db.execute(
            select(SpendingDB).where(SpendingDB.date >= start_of_month, SpendingDB.date <= today)
        )
        spendings = result.scalars().all()
        return spendings
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No spendings found for the current month"
        )


@router.post("/", response_model=Spending)
async def create_spending(spending: CreateSpending, db: AsyncSession = Depends(get_db)):
    # Fetch related currency and category from the database
    currency = await db.execute(select(CurrencyDB).where(CurrencyDB.id == spending.currency_id))
    category = await db.execute(select(CategoryDB).where(CategoryDB.id == spending.category_id))

    currency = currency.scalar_one_or_none()
    category = category.scalar_one_or_none()

    if not currency:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Currency not found")
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    new_spending = SpendingDB(**spending.model_dump(exclude_unset=True, exclude_none=True))

    db.add(new_spending)
    await db.commit()
    await db.refresh(new_spending)
    return new_spending


@router.put("/{spending_id:uuid}", response_model=Spending)
async def update_spending(
    spending_id: UUID, update_data: UpdateSpending, db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(select(SpendingDB).where(SpendingDB.id == spending_id))
        spending = result.scalar_one()

        # Update the spending attributes with the new values
        for key, value in update_data.model_dump(exclude_unset=True).items():
            setattr(spending, key, value)

        db.add(spending)
        await db.commit()
        await db.refresh(spending)
        return spending
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Spending not found")


@router.delete("/{spending_id:uuid}", response_model=dict)
async def delete_spending(spending_id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(SpendingDB).where(SpendingDB.id == spending_id))
        spending = result.scalar_one()
        await db.delete(spending)
        await db.commit()
        return {"message": "Spending deleted successfully"}
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Spending not found")
