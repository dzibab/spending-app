from datetime import datetime

from app.db.models import Spending


def test_create_spending(session):
    # Use a datetime object for the date field
    new_spending = Spending(
        amount=19.99,
        date=datetime(2024, 10, 17, 12, 0, 0),  # Correct datetime object
        currency="USD",
        category="Food"
    )

    session.add(new_spending)  # Use the session fixture
    session.commit()
    session.refresh(new_spending)

    # Query to ensure the spending was added
    spending = session.query(Spending).filter(Spending.id == new_spending.id).first()

    assert spending is not None
    assert spending.amount == 19.99
    assert spending.currency == "USD"
    assert spending.category == "Food"
    assert spending.date == datetime(2024, 10, 17, 12, 0, 0)  # Correct datetime comparison
