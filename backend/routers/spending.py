from uuid import UUID
from datetime import date

from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    Query,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound

from backend.db.models import (
    Spending as SpendingDB,
    Currency as CurrencyDB,
    Category as CategoryDB,
)
from backend.db.session import get_db
from backend.models.spending import (
    CreateSpending,
    UpdateSpending,
    SpendingResponse,
)


router = APIRouter(prefix="/spending", tags=["spending"])


async def get_spending_by_id(spending_id: UUID, db: AsyncSession):
    try:
        result = await db.execute(select(SpendingDB).where(SpendingDB.id == spending_id))
        return result.scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Spending not found")


@router.get("/", response_model=list[SpendingResponse])
async def get_spendings(
    db: AsyncSession = Depends(get_db),
    start_date: date | None = Query(None, description="Start date for filtering spendings"),
    end_date: date | None = Query(None, description="End date for filtering spendings"),
):
    query = select(SpendingDB)

    if start_date:
        query = query.where(SpendingDB.date >= start_date)
    if end_date:
        query = query.where(SpendingDB.date <= end_date)

    result = await db.execute(query)
    spendings = result.scalars().all()
    return [
        SpendingResponse.model_validate(spending, from_attributes=True) for spending in spendings
    ]


@router.get("/{spending_id:uuid}", response_model=SpendingResponse)
async def get_spending(spending_id: UUID, db: AsyncSession = Depends(get_db)):
    spending = await get_spending_by_id(spending_id, db)
    return SpendingResponse.model_validate(spending, from_attributes=True)


@router.get("/current-month", response_model=list[SpendingResponse])
async def get_spendings_current_month(db: AsyncSession = Depends(get_db)):
    today = date.today()
    start_of_month = today.replace(day=1)

    result = await db.execute(
        select(SpendingDB).where(SpendingDB.date >= start_of_month, SpendingDB.date <= today)
    )
    spendings = result.scalars().all()
    return [
        SpendingResponse.model_validate(spending, from_attributes=True) for spending in spendings
    ]


@router.post("/", response_model=SpendingResponse)
async def create_spending(spending: CreateSpending, db: AsyncSession = Depends(get_db)):
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
    return SpendingResponse.model_validate(new_spending, from_attributes=True)


@router.put("/{spending_id:uuid}", response_model=SpendingResponse)
async def update_spending(
    spending_id: UUID, update_data: UpdateSpending, db: AsyncSession = Depends(get_db)
):
    spending = await get_spending_by_id(spending_id, db)

    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(spending, key, value)

    db.add(spending)
    await db.commit()
    await db.refresh(spending)
    return SpendingResponse.model_validate(spending, from_attributes=True)


@router.delete("/{spending_id:uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_spending(spending_id: UUID, db: AsyncSession = Depends(get_db)):
    spending = await get_spending_by_id(spending_id, db)
    await db.delete(spending)
    await db.commit()
