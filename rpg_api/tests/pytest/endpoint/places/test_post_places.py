import pytest
from httpx import AsyncClient
from fastapi import status
from rpg_api.utils.daos import AllDAOs

from rpg_api.db.postgres.factory import factories
from rpg_api.tests.pytest.test_utils import get_data
from rpg_api import constants

url = "/api/postgres/places"


@pytest.mark.anyio
async def test_create_place(
    client: AsyncClient,
    daos: AllDAOs,
) -> None:
    """Test create place: 201."""

    input_json = {
        "name": "Place",
        "description": "Description",
        "radius": 1.0,
        "x": 2,
        "y": 3,
    }

    response = await client.post(url, json=input_json)
    assert response.status_code == status.HTTP_201_CREATED

    response_data = get_data(response)
    db_place = await daos.place.filter_first(id=response_data)

    assert db_place
    assert db_place.name == input_json["name"]
    assert db_place.description == input_json["description"]
    assert db_place.radius == input_json["radius"]
    assert db_place.x == input_json["x"]
    assert db_place.y == input_json["y"]


@pytest.mark.anyio
async def test_create_place_name_taken(
    client: AsyncClient,
) -> None:
    """Test create place: 400."""

    input_json = {
        "name": "Place",
    }

    await factories.PlaceFactory.create(name=input_json["name"])

    response = await client.post(url, json=input_json)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Place name already taken"


@pytest.mark.anyio
@pytest.mark.parametrize(
    "place_radius, expected_status",
    [
        # Overlap
        (10.1, status.HTTP_400_BAD_REQUEST),
        (10.0, status.HTTP_400_BAD_REQUEST),
        # No overlap
        (9.99, status.HTTP_201_CREATED),
        (9.98, status.HTTP_201_CREATED),
    ],
)
async def test_create_place_overlaps(
    client: AsyncClient,
    place_radius: float,
    expected_status: int,
) -> None:
    """Test create place: 201/400."""

    await factories.PlaceFactory.create(radius=10.0)

    input_json = {
        "name": "Place",
        "radius": place_radius,
        "x": 20,
    }

    response = await client.post(url, json=input_json)
    assert response.status_code == expected_status


@pytest.mark.anyio
@pytest.mark.parametrize(
    "input_json",
    [
        # Invalid equivalence classes
        {"name": "a" * (constants.MIN_LENGTH_PLACE_NAME - 1)},
        {"name": "a" * (constants.MIN_LENGTH_PLACE_NAME - 2)},
        {"name": "a" * (constants.MAX_LENGTH_PLACE_NAME + 1)},
        {"name": "a" * (constants.MAX_LENGTH_PLACE_NAME + 1)},
        {"name": "a" * (constants.MAX_LENGTH_PLACE_NAME + 2)},
        # Invalid types
        {},  # Missing required fields
        {"name": 123},  # Invalid type
        {"name": "Place", "radius": "invalid_value"},  # Invalid type
        {"name": "Place", "x": "invalid_value"},  # Invalid type
        {"name": "Place", "y": "invalid_value"},  # Invalid type
    ],
)
async def test_create_place_invalid_input(
    client: AsyncClient, input_json: dict[str, str]
) -> None:
    """Test create place: 422."""

    response = await client.post(url, json=input_json)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
