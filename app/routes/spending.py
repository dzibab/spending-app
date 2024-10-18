from typing import Optional
from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.spending import SpendingCreate, SpendingUpdate, Spending as SpendingResponse
from app.db.models import Spending as SpendingDB


router = APIRouter()


# Helper function to fetch spending by ID
def fetch_spending(spending_id: int, db: Session) -> SpendingDB:
    spending = db.query(SpendingDB).filter(SpendingDB.id == spending_id).first()
    if not spending:
        raise HTTPException(status_code=404, detail="Spending not found")
    return spending


@router.post(
    "/spendings/",
    response_model=SpendingResponse,
    summary="Add a new spending",
    description="Creates a new spending record with the provided details.",
)
def add_spending(spending: SpendingCreate, db: Session = Depends(get_db)):
    new_spending = SpendingDB(**spending.model_dump())
    db.add(new_spending)
    db.commit()
    db.refresh(new_spending)
    return new_spending


@router.get(
    "/spendings/{spending_id}",
    response_model=SpendingResponse,
    summary="Get a spending",
    description="Retrieves a spending record by its ID.",
)
def get_spending(spending_id: int, db: Session = Depends(get_db)):
    return fetch_spending(spending_id, db)


@router.get(
    "/spendings/",
    response_model=dict,
    summary="Get spendings",
    description="Retrieves a list of spending records with pagination and optional filtering.",
)
def get_spendings(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    description: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    currency: Optional[str] = None,
    category: Optional[str] = None,
    amount: Optional[float] = None,
    db: Session = Depends(get_db)
):
    query = db.query(SpendingDB)

    # Apply filters if provided
    if description:
        query = query.filter(SpendingDB.description.ilike(f"%{description}%"))
    if start_date:
        start_datetime = datetime.combine(start_date, datetime.min.time())
        query = query.filter(SpendingDB.date >= start_datetime)
    if end_date:
        end_datetime = datetime.combine(end_date, datetime.max.time())
        query = query.filter(SpendingDB.date <= end_datetime)
    if currency:
        query = query.filter(SpendingDB.currency == currency)
    if category:
        query = query.filter(SpendingDB.category == category)
    if amount:
        query = query.filter(SpendingDB.amount == amount)

    total = query.count()
    spendings = query.offset(skip).limit(limit).all()

    # Convert spendings to SpendingResponse model
    spendings_response = [SpendingResponse.model_validate(spending) for spending in spendings]

    return {"spendings": spendings_response, "total": total}


@router.put(
    "/spendings/{spending_id}",
    response_model=SpendingResponse,
    summary="Update a spending",
    description="Updates a spending record by its ID.",
)
def update_spending(spending_id: int, updated_data: SpendingUpdate, db: Session = Depends(get_db)):
    spending = fetch_spending(spending_id, db)

    # Update fields if new values are provided
    for field, value in updated_data.model_dump(exclude_unset=True).items():
        setattr(spending, field, value)

    db.commit()
    db.refresh(spending)
    return spending


@router.delete(
    "/spendings/{spending_id}",
    summary="Delete a spending",
    description="Deletes a spending record by its ID.",
)
def delete_spending(spending_id: int, db: Session = Depends(get_db)):
    spending = fetch_spending(spending_id, db)
    db.delete(spending)
    db.commit()
    return {"detail": "Spending deleted successfully"}
