import pytest
from httpx import AsyncClient
from fastapi import Response, status
from rpg_api import constants
from rpg_api.db.postgres.factory import factories
from rpg_api.tests.pytest import test_utils
from rpg_api.utils.daos import AllDAOs
from rpg_api.utils.dtos import CharacterLocationUpdateDTO
import uuid

url = "/api/postgres/characters/place"


@pytest.mark.anyio
async def test_get_character_place_wilderness(client: AsyncClient) -> None:
    """Test get character in an unnamed place (Wilderness): 200."""

    user = await factories.BaseUserFactory.create()
    user_header = test_utils.get_user_header(user.id)

    character = await factories.CharacterFactory.create(user=user)

    response = await client.get(f"{url}/{character.id}", headers=user_header)
    assert response.status_code == status.HTTP_200_OK

    response_data = test_utils.get_data(response)
    assert response_data["name"] == "Wilderness"


@pytest.mark.anyio
@pytest.mark.parametrize(
    "x_coordinate, y_coordinate",
    [
        (0, 0),
        (0, constants.INT32_MAX),
        (
            constants.INT32_MAX,
            0,
        ),
        (-1000, 1000),
        (-100, -100),
        (100, 100),
    ],
)
async def test_get_character_place_named_place(
    client: AsyncClient,
    daos: AllDAOs,
    x_coordinate: int,
    y_coordinate: int,
) -> None:
    """Test get character on the exact coordinates of a named place: 200."""

    user = await factories.BaseUserFactory.create()
    user_header = test_utils.get_user_header(user.id)

    await factories.PlaceFactory.create(
        name="Goldshire", radius=0, x=x_coordinate, y=y_coordinate
    )
    character = await factories.CharacterFactory.create(user=user)
    assert character.character_location_id is not None
    character_location = await daos.character_location.get_by_id(
        character.character_location_id
    )
    update_data = CharacterLocationUpdateDTO(x=x_coordinate, y=y_coordinate)
    await daos.character_location.update(character_location.id, update_data)
    assert character.character_location is not None
    assert character.character_location.x == x_coordinate
    assert character.character_location.y == y_coordinate

    response = await client.get(f"{url}/{character.id}", headers=user_header)
    assert response.status_code == status.HTTP_200_OK

    response_data = test_utils.get_data(response)
    assert response_data["name"] == "Goldshire"


@pytest.mark.anyio
@pytest.mark.parametrize(
    "x_character, y_character, radius_place, x_place, y_place",
    [
        (10, 0, 10.000001, 0, 0),
        (0, 10, 10.000002, 0, 0),
        (-10, 0, 10.000001, -10, -10),
        (0, -10, 10.000002, -10, -10),
        ((constants.INT32_MAX - 1), 0, 1.000001, (constants.INT32_MAX - 2), 0),
        (0, (constants.INT32_MAX - 1), 1.000002, 0, (constants.INT32_MAX - 2)),
        ((constants.INT32_MIN + 1), 0, 1.000001, (constants.INT32_MIN + 2), 0),
        (0, (constants.INT32_MIN + 1), 1.000002, 0, (constants.INT32_MIN + 2)),
        (5, 5, 10.5, 0, 0),
        (-5, -5, 10.5, 0, 0),
        (5, 5, 10, 0, 0),
    ],
)
async def test_get_character_place_named_place_radius_inside_boundary(
    client: AsyncClient,
    daos: AllDAOs,
    x_character: int,
    y_character: int,
    radius_place: float,
    x_place: int,
    y_place: int,
) -> None:
    """Test get character in the radius of a named place: 200."""

    user = await factories.BaseUserFactory.create()
    user_header = test_utils.get_user_header(user.id)

    await factories.PlaceFactory.create(
        name="Goldshire", radius=radius_place, x=x_place, y=y_place
    )
    character = await factories.CharacterFactory.create(user=user)
    assert character.character_location_id is not None
    character_location = await daos.character_location.get_by_id(
        character.character_location_id
    )
    update_data = CharacterLocationUpdateDTO(x=x_character, y=y_character)
    await daos.character_location.update(character_location.id, update_data)
    assert character.character_location is not None
    assert character.character_location.x == x_character
    assert character.character_location.y == y_character

    response = await client.get(f"{url}/{character.id}", headers=user_header)
    assert response.status_code == status.HTTP_200_OK

    response_data = test_utils.get_data(response)
    assert response_data["name"] == "Goldshire"


@pytest.mark.anyio
@pytest.mark.parametrize(
    "x_character, y_character, radius_place, x_place, y_place",
    [
        (10, 0, 9.999999, 0, 0),
        (0, 10, 9.999998, 0, 0),
        (-10, 0, 9.999999, -10, -10),
        (0, -10, 9.999998, -10, -10),
        ((constants.INT32_MAX - 1), 0, 0.999999, (constants.INT32_MAX - 2), 0),
        (0, (constants.INT32_MAX - 1), 0.999998, 0, (constants.INT32_MAX - 2)),
        ((constants.INT32_MIN + 1), 0, 0.999999, (constants.INT32_MIN + 2), 0),
        (0, (constants.INT32_MIN + 1), 0.999998, 0, (constants.INT32_MIN + 2)),
        (10, 10, 9.5, 0, 0),
        (-10, -10, 9.5, 0, 0),
        (10, 10, 9, 0, 0),
    ],
)
async def test_get_character_place_named_place_outside_radius_boundary(
    client: AsyncClient,
    daos: AllDAOs,
    x_character: int,
    y_character: int,
    radius_place: float,
    x_place: int,
    y_place: int,
) -> None:
    """Test get character in an invalid EP boundary of the radius: 200."""

    user = await factories.BaseUserFactory.create()
    user_header = test_utils.get_user_header(user.id)

    await factories.PlaceFactory.create(
        name="Goldshire", radius=radius_place, x=x_place, y=y_place
    )
    character = await factories.CharacterFactory.create(user=user)
    assert character.character_location_id is not None
    character_location = await daos.character_location.get_by_id(
        character.character_location_id
    )
    update_data = CharacterLocationUpdateDTO(x=x_character, y=y_character)
    await daos.character_location.update(character_location.id, update_data)
    assert character.character_location is not None
    assert character.character_location.x == x_character
    assert character.character_location.y == y_character

    response = await client.get(f"{url}/{character.id}", headers=user_header)
    assert response.status_code == status.HTTP_200_OK

    response_data = test_utils.get_data(response)
    assert response_data["name"] == "Wilderness"


@pytest.mark.anyio
async def test_get_character_place_invalid_character(client: AsyncClient) -> None:
    """Test get character in a place with invalid character id: 404."""

    user = await factories.BaseUserFactory.create()
    user_header = test_utils.get_user_header(user.id)

    invalid_id = uuid.uuid4()

    response = await client.get(f"{url}/{invalid_id}", headers=user_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.anyio
async def test_get_character_place_invalid_token(client: AsyncClient) -> None:
    """Test get character in a place with invalid token: 401."""

    user = await factories.BaseUserFactory.create()
    user_header = {"Authorization": "Bearer invalid"}

    character = await factories.CharacterFactory.create(user=user)

    response = await client.get(f"{url}/{character.id}", headers=user_header)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
async def test_get_character_place_no_token(client: AsyncClient) -> None:
    """Test get character in a place with no token: 401."""

    user = await factories.BaseUserFactory.create()

    character = await factories.CharacterFactory.create(user=user)

    response = await client.get(f"{url}/{character.id}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
@pytest.mark.parametrize(
    "method",
    [
        "post",
        "put",
        "delete",
        "patch",
        "options",
        "head",
    ],
)
async def test_character_place_method_not_allowed(
    client: AsyncClient, method: str
) -> None:
    """
    Test that various HTTP methods are not
    allowed for the character place endpoint: 405.
    """

    http_method = getattr(client, method)
    character_id = uuid.uuid4()

    response: Response = await http_method(f"{url}/{character_id}")
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
