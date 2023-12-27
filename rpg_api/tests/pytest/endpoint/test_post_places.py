import pytest
from httpx import AsyncClient
from fastapi import status
from rpg_api.db.postgres.factory import factories
from rpg_api.tests.pytest import test_utils

url = "/api/postgres/places"


@pytest.mark.anyio
async def test_get_places_empty_list(client: AsyncClient) -> None:
    "Test get all places with 0 places in the database: 200."

    user = await factories.BaseUserFactory.create()
    header = test_utils.get_user_header(user.id)

    response = await client.get(url, headers=header)
    assert response.status_code == status.HTTP_200_OK

    response_data = test_utils.get_data(response)
    assert response_data == []
    assert len(response_data) == 0


@pytest.mark.anyio
async def test_create_place(client: AsyncClient) -> None:
    "Test creating a place through the API: 201."

    user = await factories.BaseUserFactory.create()
    header = test_utils.get_user_header(user.id)

    place_data = {"name": "Miami Beach", "x": 100, "y": 200, "radius": 75}
    response = await client.post(url, headers=header, json=place_data)

    assert response.status_code == status.HTTP_201_CREATED

    response_data = test_utils.get_data(response)
    assert response_data["name"] == "Miami Beach"
    assert response_data["x"] == 100
    assert response_data["y"] == 200
    assert response_data["radius"] == 75
