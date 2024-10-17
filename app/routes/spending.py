from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db.session import get_db
from ..db.models import Spending


router = APIRouter()


@router.post("/add/")
def add_spending(
        description: str,
        amount: float,
        date: datetime,
        currency: str,
        category: str,
        db: Session = Depends(get_db),
):
    new_spending = Spending(description=description, amount=amount, date=date, currency=currency, category=category)
    db.add(new_spending)
    db.commit()
    db.refresh(new_spending)
    return new_spending
