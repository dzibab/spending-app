import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_get_spendings_no_filters(test_client):
    response = test_client.get("/api/spending/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_spendings_with_start_date_filter(test_client):
    response = test_client.get("/api/spending/", params={"start_date": "2023-01-01"})
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_spendings_with_end_date_filter(test_client):
    response = test_client.get("/api/spending/", params={"end_date": "2023-12-31"})
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_spendings_with_date_range(test_client):
    response = test_client.get(
        "/api/spending/", params={"start_date": "2023-01-01", "end_date": "2023-12-31"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
