from datetime import datetime

from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Spending Tracker!"}


def test_get_spending(client, session):
    # First, create a spending to retrieve
    spending_data = {
        "description": "Test Get Spending",
        "amount": 50.00,
        "date": datetime(2024, 10, 17, 12, 0, 0).isoformat(),
        "currency": "EUR",
        "category": "Groceries"
    }
    response = client.post("/spendings/", json=spending_data)
    assert response.status_code == 200
    spending_id = response.json()["id"]

    # Now, retrieve the spending
    get_response = client.get(f"/spendings/{spending_id}")

    # Validate the response
    assert get_response.status_code == 200
    data = get_response.json()

    assert data["id"] == spending_id
    assert data["description"] == "Test Get Spending"
    assert data["amount"] == 50.00
    assert data["date"] == "2024-10-17T12:00:00"
    assert data["currency"] == "EUR"
    assert data["category"] == "Groceries"


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


def test_update_spending(client, session):
    # First, create a spending to update
    spending_data = {
        "description": "Test Spending",
        "amount": 29.99,
        "date": datetime(2024, 10, 17, 14, 0, 0).isoformat(),
        "currency": "USD",
        "category": "Entertainment"
    }
    response = client.post("/spendings/", json=spending_data)
    spending_id = response.json()["id"]

    # Update the spending
    update_data = {
        "description": "Updated Spending",
        "amount": 49.99
    }
    update_response = client.put(f"/spendings/{spending_id}", json=update_data)

    assert update_response.status_code == 200
    updated_spending = update_response.json()

    assert updated_spending["description"] == "Updated Spending"
    assert updated_spending["amount"] == 49.99


def test_delete_spending(client, session):
    # First, create a spending to delete
    spending_data = {
        "description": "Test Spending",
        "amount": 29.99,
        "date": datetime(2024, 10, 17, 14, 0, 0).isoformat(),
        "currency": "USD",
        "category": "Entertainment"
    }
    response = client.post("/spendings/", json=spending_data)
    spending_id = response.json()["id"]

    # Delete the spending
    delete_response = client.delete(f"/spendings/{spending_id}")

    assert delete_response.status_code == 200
    assert delete_response.json() == {"detail": "Spending deleted successfully"}

    # Verify that the spending no longer exists
    get_response = client.get(f"/spendings/{spending_id}")
    assert get_response.status_code == 404  # Expect 404 since it should be deleted


def test_get_spendings(client, session):
    # Add some test spendings
    for i in range(20):  # Add 20 records
        spending_data = {
            "description": f"Test Spending {i}",
            "amount": 10.0,
            "date": datetime(2024, 10, 17, 14, 0, 0).isoformat(),
            "currency": "USD",
            "category": "Food"
        }
        client.post("/spendings/", json=spending_data)

    # Request the first 10 spendings
    response = client.get("/spendings/?skip=0&limit=10")
    assert response.status_code == 200
    assert len(response.json()["spendings"]) == 10  # Expecting 10 records
    assert response.json()["total"] == 20  # Total should be 20

    # Request the next 10 spendings
    response = client.get("/spendings/?skip=10&limit=10")
    assert response.status_code == 200
    assert len(response.json()["spendings"]) == 10  # Expecting 10 records
    assert response.json()["total"] == 20  # Total should still be 20

    # Requesting beyond the total count
    response = client.get("/spendings/?skip=30&limit=10")
    assert response.status_code == 200
    assert len(response.json()["spendings"]) == 0  # Expecting 0 records
    assert response.json()["total"] == 20  # Total should still be 20


def test_get_spendings_with_date_range(client, session):
    # Add some test spendings
    for i in range(20):
        spending_data = {
            "description": f"Test Spending {i}",
            "amount": 10.0 + i,
            "date": datetime(2024, 10, 17, 14, 0, 0).isoformat(),  # Same date for simplicity
            "currency": "USD",
            "category": "Food"
        }
        client.post("/spendings/", json=spending_data)

    # Test filtering by date range
    response = client.get("/spendings/?start_date=2024-10-17&end_date=2024-10-17&limit=20")
    assert response.status_code == 200
    assert len(response.json()["spendings"]) == 20  # Expecting 20 records

    # Test filtering with a different date range
    response = client.get("/spendings/?start_date=2024-10-16&end_date=2024-10-18&limit=20")
    assert response.status_code == 200
    assert len(response.json()["spendings"]) == 20  # Expecting 20 records (as they all fall in this range)


def test_get_spendings_with_all_filters(client, session):
    # Add test spendings
    spendings_data = [
        {"description": "Groceries", "amount": 50.0, "date": "2024-10-17", "currency": "USD", "category": "Food"},
        {"description": "Dinner", "amount": 30.0, "date": "2024-10-17", "currency": "USD", "category": "Food"},
        {"description": "Cinema", "amount": 15.0, "date": "2024-10-18", "currency": "USD", "category": "Entertainment"},
        {"description": "Gas", "amount": 40.0, "date": "2024-10-19", "currency": "USD", "category": "Transport"},
        {"description": "Book", "amount": 20.0, "date": "2024-10-20", "currency": "USD", "category": "Education"},
        {"description": "Grocery", "amount": 25.0, "date": "2024-10-20", "currency": "USD", "category": "Food"},
    ]

    # Post all spendings
    for spending in spendings_data:
        client.post("/spendings/", json=spending)

    # Test filtering by description (partial match)
    response = client.get("/spendings/?description=Gro")
    assert response.status_code == 200
    assert len(response.json()["spendings"]) == 2  # Expecting 2 records (Groceries, Grocery)

    # Test filtering by date range
    response = client.get("/spendings/?start_date=2024-10-17&end_date=2024-10-19")
    assert response.status_code == 200
    assert len(response.json()["spendings"]) == 4  # Expecting 4 records (2 from 17th, 1 from 18th, and 1 from 19th)

    # Test filtering by currency
    response = client.get("/spendings/?currency=USD")
    assert response.status_code == 200
    assert len(response.json()["spendings"]) == 6  # Expecting 6 records

    # Test filtering by category
    response = client.get("/spendings/?category=Food")
    assert response.status_code == 200
    assert len(response.json()["spendings"]) == 3  # Expecting 3 records

    # Test filtering by amount
    response = client.get("/spendings/?amount=50.0")
    assert response.status_code == 200
    assert len(response.json()["spendings"]) == 1  # Expecting 1 record (Groceries)

    # Test combination of filters
    response = client.get(
        "/spendings/?description=Gro&start_date=2024-10-17&end_date=2024-10-20&currency=USD&category=Food&amount=50.0"
    )
    assert response.status_code == 200
    assert len(response.json()["spendings"]) == 1  # Expecting 1 record (Groceries)

    # Test with skip and limit parameters
    response = client.get("/spendings/?skip=1&limit=2")
    assert response.status_code == 200
    assert len(response.json()["spendings"]) == 2  # Expecting 2 records
