from uuid import uuid4

import pytest
from fastapi import status

from backend.enums import CategoryEnum


@pytest.fixture
def create_category(test_client):
    response = test_client.post("/api/category/", json={"name": "Test_Category"})
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()["id"]


@pytest.mark.asyncio
async def test_get_all_categories(test_client):
    response = test_client.get("/api/category/")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # add categories
    for category in CategoryEnum:
        response = test_client.post("/api/category/", json={"name": category.value})
        assert response.status_code == status.HTTP_201_CREATED

    # verify categories can be retrieved
    response = test_client.get("/api/category/")
    categories = response.json()
    assert isinstance(categories, list)
    assert len(categories) == len(CategoryEnum)


@pytest.mark.asyncio
async def test_create_category(test_client):
    test_category = "test_create_category"
    response = test_client.post("/api/category/", json={"name": test_category})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == test_category.capitalize()
    assert response.json()["id"]


@pytest.mark.asyncio
async def test_create_category_invalid(test_client):
    response = test_client.post("/api/category/", json={})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_get_category_method_not_allowed(test_client):
    category_id = uuid4()
    response = test_client.get(f"/api/category/{category_id}")
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.asyncio
async def test_delete_category(test_client, create_category):
    category_id = str(create_category)
    response = test_client.delete(f"/api/category/{category_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
