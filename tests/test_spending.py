from datetime import datetime

from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Spending Tracker!"}


def test_add_spending(client):
    spending_data = {
        "description": "Test Spending",
        "amount": 29.99,
        "date": datetime(2024, 10, 17, 14, 0, 0).isoformat(),  # Convert datetime to ISO 8601 string
        "currency": "USD",
        "category": "Entertainment"
    }

    response = client.post("/spendings/", json=spending_data)

    assert response.status_code == 200
    result = response.json()

    assert result["amount"] == 29.99
    assert result["currency"] == "USD"
    assert result["category"] == "Entertainment"

    # Convert the returned date back to a datetime object for comparison
    assert datetime.fromisoformat(result["date"]) == datetime(2024, 10, 17, 14, 0, 0)
