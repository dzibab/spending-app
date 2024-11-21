from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound

from src.db.models import Spending as SpendingDB, Currency as CurrencyDB, Category as CategoryDB
from src.db.session import get_db
from src.models.spending import CreateSpending, UpdateSpending, Spending


router = APIRouter(prefix="/spending", tags=["spending"])


@router.get("/", response_model=list[Spending])
async def get_spendings(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SpendingDB))
    spendings = result.scalars().all()
    return spendings


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

    # Create new spending entry
    new_spending = SpendingDB(
        amount=spending.amount,
        date=spending.date,
        currency_id=spending.currency_id,
        category_id=spending.category_id,
        description=spending.description,
    )

    db.add(new_spending)
    await db.commit()
    await db.refresh(new_spending)
    return new_spending


@router.get("/{spending_id}", response_model=Spending)
async def get_spending(spending_id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(SpendingDB).where(SpendingDB.id == spending_id))
        spending = result.scalar_one()
        return spending
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Spending not found")


@router.put("/{spending_id}", response_model=Spending)
async def update_spending(
    spending_id: UUID, update_data: UpdateSpending, db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(select(SpendingDB).where(SpendingDB.id == spending_id))
        spending = result.scalar_one()

        # Update the spending attributes with the new values
        for key, value in update_data.model_dump(exclude_unset=True).items():
            setattr(spending, key, value)

        # Commit and refresh
        db.add(spending)
        await db.commit()
        await db.refresh(spending)
        return spending
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Spending not found")


@router.delete("/{spending_id}", response_model=dict)
async def delete_spending(spending_id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(SpendingDB).where(SpendingDB.id == spending_id))
        spending = result.scalar_one()
        await db.delete(spending)
        await db.commit()
        return {"message": "Spending deleted successfully"}
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Spending not found")
