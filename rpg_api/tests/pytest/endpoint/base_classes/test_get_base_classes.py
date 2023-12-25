import pytest
from httpx import AsyncClient
from fastapi import status
from rpg_api.db.postgres.factory import factories
from typing import Any

url = "/api/postgres/base-classes"


def get_user_header(token: str) -> dict[str, Any]:
    """Return access token for given data."""
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.anyio
async def test_get_base_classes_empty_list(client: AsyncClient) -> None:
    """Test get all base classes with 0 base classes in the database: 200."""

    response = await client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"] == []
    assert len(response.json()["data"]) == 0


@pytest.mark.anyio
async def test_get_base_classes_populated_list(client: AsyncClient) -> None:
    """Test get all base classes with 1 base class in the database: 200."""

    baseClass = await factories.BaseClassFactory.create()

    response = await client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"][0]["id"] == str(baseClass.id)
    assert response.json()["data"][0]["name"] == baseClass.name


@pytest.mark.anyio
async def test_get_base_classes_populated_list_2(client: AsyncClient) -> None:
    """Test get all base classes with 2 base classes in the database: 200."""

    baseClass1 = await factories.BaseClassFactory.create()
    baseClass2 = await factories.BaseClassFactory.create()

    response = await client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"][0]["id"] == str(baseClass1.id)
    assert response.json()["data"][0]["name"] == baseClass1.name
    assert response.json()["data"][1]["id"] == str(baseClass2.id)
    assert response.json()["data"][1]["name"] == baseClass2.name
    assert len(response.json()["data"]) == 2


@pytest.mark.anyio
async def test_base_classes_method_not_allowed_post(client: AsyncClient) -> None:
    """Test that POST method is not allowed for the base-classes endpoint."""

    response = await client.post(url, json={"name": "NewClass"})

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.anyio
async def test_base_classes_method_not_allowed_put(client: AsyncClient) -> None:
    """Test that PUT method is not allowed for the base-classes endpoint."""

    response = await client.put(url, json={"name": "UpdatedClass"})

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.anyio
async def test_base_classes_method_not_allowed_delete(client: AsyncClient) -> None:
    """Test that DELETE method is not allowed for the base-classes endpoint."""

    response = await client.delete(url)

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.anyio
async def test_base_classes_method_not_allowed_patch(client: AsyncClient) -> None:
    """Test that PATCH method is not allowed for the base-classes endpoint."""

    response = await client.patch(url, json={"name": "PatchedClass"})

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.anyio
async def test_base_classes_method_not_allowed_options(client: AsyncClient) -> None:
    """Test that OPTIONS method is not allowed for the base-classes endpoint."""

    response = await client.options(url)

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.anyio
async def test_base_classes_method_not_allowed_head(client: AsyncClient) -> None:
    """Test that HEAD method is not allowed for the base-classes endpoint."""

    response = await client.head(url)

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
