import pytest
from httpx import AsyncClient
from fastapi import Response, status
from rpg_api.db.postgres.factory import factories
from rpg_api.tests.pytest.test_utils import get_data
from rpg_api.utils import models
from typing import Any

url = "/api/postgres/places"


def _assert_place_data(
    response_data: dict[str, Any],
    place: models.Place,
) -> None:
    """Assert place data."""
    assert response_data["id"] == str(place.id)
    assert response_data["name"] == place.name
    assert response_data["description"] == place.description
    assert response_data["x"] == place.x
    assert response_data["y"] == place.y
    assert response_data["radius"] == place.radius


@pytest.mark.anyio
@pytest.mark.parametrize("create_num", [0, 1, 2])
async def test_get_all_places(client: AsyncClient, create_num: int) -> None:
    """Test get all places: 200."""

    # x = i is used to avoid overlapping places
    places = [await factories.PlaceFactory.create(x=i) for i in range(create_num)]

    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK

    response_data = get_data(response)
    assert len(response_data) == create_num

    for index, place in enumerate(places):
        _assert_place_data(response_data[index], place)


@pytest.mark.anyio
async def test_get_all_places_by_search(
    client: AsyncClient,
) -> None:
    """Test get all places by search: 200."""

    places = [
        await factories.PlaceFactory.create(
            name="Test to be found",
            description="This is a test that should be found",
            x=1,
        ),
        await factories.PlaceFactory.create(
            name="Also test to be found",
            description="This is another test that should be found",
            x=2,
        ),
    ]

    # This place should not be found
    await factories.PlaceFactory.create(
        name="Random name",
        description="This is a random description",
        x=3,
    )

    response = await client.get(url, params={"search": "test should"})
    assert response.status_code == status.HTTP_200_OK

    response_data = get_data(response)
    assert len(response_data) == len(places)

    for index, place in enumerate(places):
        _assert_place_data(response_data[index], place)


@pytest.mark.anyio
@pytest.mark.parametrize(
    "method",
    [
        "put",
        "delete",
        "patch",
        "options",
        "head",
    ],
)
async def test_place_method_not_allowed(client: AsyncClient, method: str) -> None:
    """
    Test for method that are not allowed.
    """

    http_method = getattr(client, method)

    response: Response = await http_method(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
