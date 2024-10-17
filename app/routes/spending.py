from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.spending import SpendingCreate
from app.db import models


router = APIRouter()


@router.post("/spendings/")
def add_spending(spending: SpendingCreate, db: Session = Depends(get_db)):
    new_spending = models.Spending(
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
