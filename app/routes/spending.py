from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.spending import SpendingCreate, SpendingUpdate
from app.db.models import Spending


router = APIRouter()


@router.post("/spendings/")
def add_spending(spending: SpendingCreate, db: Session = Depends(get_db)):
    new_spending = Spending(
        description=spending.description,
        amount=spending.amount,
        date=spending.date,
        currency=spending.currency,
        category=spending.category
    )
    db.add(new_spending)
    db.commit()
    db.refresh(new_spending)
    return new_spending


# GET route to fetch a spending by ID
@router.get("/spendings/{spending_id}")
def get_spending(spending_id: int, db: Session = Depends(get_db)):
    spending = db.query(Spending).filter(Spending.id == spending_id).first()
    if not spending:
        raise HTTPException(status_code=404, detail="Spending not found")
    return spending


# Update Spending
@router.put("/spendings/{spending_id}")
def update_spending(spending_id: int, updated_data: SpendingUpdate, db: Session = Depends(get_db)):
    spending = db.query(Spending).filter(Spending.id == spending_id).first()

    if not spending:
        raise HTTPException(status_code=404, detail="Spending not found")

    # Update fields if new values are provided
    if updated_data.description is not None:
        spending.description = updated_data.description
    if updated_data.amount is not None:
        spending.amount = updated_data.amount
    if updated_data.date is not None:
        spending.date = updated_data.date
    if updated_data.currency is not None:
        spending.currency = updated_data.currency
    if updated_data.category is not None:
        spending.category = updated_data.category

    db.commit()
    db.refresh(spending)
    return spending


# Delete Spending
@router.delete("/spendings/{spending_id}")
def delete_spending(spending_id: int, db: Session = Depends(get_db)):
    spending = db.query(Spending).filter(Spending.id == spending_id).first()
    if not spending:
        raise HTTPException(status_code=404, detail="Spending not found")

    db.delete(spending)
    db.commit()

    return {"detail": "Spending deleted successfully"}
