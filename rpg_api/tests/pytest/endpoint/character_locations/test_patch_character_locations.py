from typing import Any
import pytest
from httpx import AsyncClient
from fastapi import Response, status
from rpg_api import constants
from rpg_api.db.postgres.factory import factories
from rpg_api.tests.pytest import test_utils
import uuid


url = "/api/postgres/character-locations"


@pytest.mark.anyio
@pytest.mark.parametrize(
    "x, y",
    [
        (constants.INT32_MAX, 0),
        (constants.INT32_MIN, 0),
        (0, constants.INT32_MAX),
        (0, constants.INT32_MIN),
        (constants.INT32_MAX - 1, 0),
        (constants.INT32_MIN + 1, 0),
        (0, constants.INT32_MAX - 1),
        (0, constants.INT32_MIN + 1),
        (0, 0),
        (100, 100),
        (-100, -100),
    ],
)
async def test_patch_character_location_valid_boundaries(
    client: AsyncClient, x: int, y: int
) -> None:
    """Test updating character location with valid boundaries: 200."""

    user = await factories.BaseUserFactory.create()
    user_header = test_utils.get_user_header(user.id)

    character = await factories.CharacterFactory.create(user=user)
    # This ensures mypy knows that character_location is not None
    assert character.character_location is not None
    character_location = {"x": x, "y": y}

    response = await client.patch(
        f"{url}/{character.id}", headers=user_header, json=character_location
    )
    assert response.status_code == status.HTTP_200_OK

    assert character.character_location.x == x
    assert character.character_location.y == y


@pytest.mark.anyio
async def test_patch_character_location_updating_one_coordinate(
    client: AsyncClient,
) -> None:
    """Test updating character location with one missing coordinate: 200."""

    user = await factories.BaseUserFactory.create()
    user_header = test_utils.get_user_header(user.id)

    character = await factories.CharacterFactory.create(user=user)
    # This ensures mypy knows that character_location is not None
    assert character.character_location is not None
    character_location = {"x": 120}
    expected_y = character.character_location.y
    assert expected_y == 0

    response = await client.patch(
        f"{url}/{character.id}", headers=user_header, json=character_location
    )
    assert response.status_code == status.HTTP_200_OK

    assert character.character_location.x == 120
    assert character.character_location.y == expected_y


@pytest.mark.anyio
@pytest.mark.parametrize(
    "invalid_value",
    [
        "a string",
        9.99,  # float
        # True,  # boolean # GitHub Issue #73: https://github.com/kea-semester-1/Semester-Project/issues/73
        # None,  # NoneType # GitHub Issue #73: https://github.com/kea-semester-1/Semester-Project/issues/73
        [1, 2, 3],  # list
        {"x": 1},  # dict
        (1, 2),  # tuple
        (constants.INT32_MAX + 1, 0),
        (constants.INT32_MIN - 1, 0),
        (0, constants.INT32_MAX + 1),
        (0, constants.INT32_MIN - 1),
    ],
)
async def test_patch_character_location_invalid_data_type(
    client: AsyncClient, invalid_value: Any
) -> None:
    """Test updating character location with invalid data type and 0 valid ones: 422."""

    user = await factories.BaseUserFactory.create()
    user_header = test_utils.get_user_header(user.id)

    character = await factories.CharacterFactory.create(user=user)
    character_location = {"x": invalid_value}

    response = await client.patch(
        f"{url}/{character.id}", headers=user_header, json=character_location
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.anyio
async def test_patch_character_location_invalid_token(client: AsyncClient) -> None:
    """Test updating character location with invalid token: 401."""

    user = await factories.BaseUserFactory.create()
    user_header = {"Authorization": "Bearer invalid"}

    character = await factories.CharacterFactory.create(user=user)
    character_location = {"x": 0, "y": 0}

    response = await client.patch(
        f"{url}/{character.id}", headers=user_header, json=character_location
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
async def test_patch_character_location_no_token(client: AsyncClient) -> None:
    """Test updating character location with no token: 401."""

    user = await factories.BaseUserFactory.create()

    character = await factories.CharacterFactory.create(user=user)
    character_location = {"x": 0, "y": 0}

    response = await client.patch(f"{url}/{character.id}", json=character_location)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
async def test_patch_character_location_invalid_character(client: AsyncClient) -> None:
    """Test updating character location with invalid character id: 404."""

    user = await factories.BaseUserFactory.create()
    user_header = test_utils.get_user_header(user.id)

    invalid_id = uuid.uuid4()

    character_location = {"x": 0, "y": 0}

    response = await client.patch(
        f"{url}/{invalid_id}", headers=user_header, json=character_location
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.anyio
@pytest.mark.parametrize(
    "method",
    ["get", "post", "put", "delete", "options", "head"],
)
async def test_character_location_method_not_allowed(
    client: AsyncClient, method: str
) -> None:
    """
    Test that various HTTP methods are not allowed
    for the character locations endpoint: 405.
    """

    http_method = getattr(client, method)
    character_id = uuid.uuid4()

    response: Response = await http_method(f"{url}/{character_id}")
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
