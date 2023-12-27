import pytest
from httpx import AsyncClient
from fastapi import status
from rpg_api.db.postgres.factory import factories
from rpg_api.tests.pytest import test_utils

url = "/api/postgres/places"


@pytest.mark.anyio
@pytest.mark.parametrize(
    "name_place, radius, x_place, y_place",
    [
        ("Goldshire", 40, 25, -100),
        ("Stormwind City", 100, -150, 50),
        ("Ironforge", 70, 100, 100),
    ],
)
async def test_get_all_places(client: AsyncClient, name_place: str, radius: float, x_place: int, y_place: int) -> None:
    """Test get all places: 200."""

    user = await factories.BaseUserFactory.create()
    header = test_utils.get_user_header(user.id)

    place = await factories.PlaceFactory.create(name=name_place, radius=radius, x=x_place, y=y_place)
    assert place.name is not None
    assert place.radius is not None
    assert place.x is not None
    assert place.y is not None

    response = await client.get(url, headers=header)
    assert response.status_code == status.HTTP_200_OK

    response_data = test_utils.get_data(response)
    assert isinstance(response_data, list)
    assert len(response_data) == 1

    assert response_data[0]["name"] == name_place
    assert response_data[0]["radius"] == radius
    assert response_data[0]["x"] == x_place
    assert response_data[0]["y"] == y_place


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
async def test_place_method_not_allowed(
    client: AsyncClient, method: str
) -> None:
    """
    Test for method that are not allowed.
    """

    http_method = getattr(client, method)

    response = await http_method(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.anyio
async def test_get_emptyplace(client: AsyncClient) -> None:
    """Test fetching a place when there is none."""

    user = await factories.BaseUserFactory.create()
    header = test_utils.get_user_header(user.id)

    response = await client.get(url, headers=header)

    assert response.status_code == status.HTTP_200_OK
    response_data = test_utils.get_data(response)

    assert isinstance(response_data, list)
    assert len(response_data) == 0
