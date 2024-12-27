import pytest
from fastapi import status

from backend.enums import CurrencyEnum
from backend.tests.utils import random_string


@pytest.mark.asyncio
async def test_get_currencies(test_client):
    response = test_client.get("/api/currency/")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    for currency in CurrencyEnum:
        response = test_client.post("/api/currency/", json={"name": currency.value})
        assert response.status_code == status.HTTP_201_CREATED

    response = test_client.get("/api/currency/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == len(CurrencyEnum)


@pytest.mark.asyncio
async def test_create_currency(test_client):
    currency_name = random_string()
    currency_data = {"name": f"{currency_name}"}
    response = test_client.post("/api/currency/", json=currency_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == currency_name

    response = test_client.post("/api/currency/", json=currency_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_delete_currency(test_client):
    currency_name = random_string()
    response = test_client.post("/api/currency/", json={"name": currency_name})
    assert response.status_code == status.HTTP_201_CREATED

    id = response.json()["id"]
    response = test_client.delete(f"/api/currency/{id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = test_client.delete(f"/api/currency/{id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
