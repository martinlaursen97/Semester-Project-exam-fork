from typing import Any
import pytest
from httpx import AsyncClient
from fastapi import status
from rpg_api import enums
from rpg_api.db.postgres.factory import factories
from rpg_api.tests.pytest import test_utils

url = "/api/postgres/characters"


@pytest.mark.anyio
async def test_create_character_success(client: AsyncClient) -> None:
    """Test successful character creation: 201."""

    user = await factories.BaseUserFactory.create()
    user_header = test_utils.get_user_header(user.id)

    base_class = await factories.BaseClassFactory.create()
    character_data = {
        "base_class_id": str(base_class.id),
        "gender": enums.Gender.male,
        "character_name": "Garrosh Hellscream",
    }

    response = await client.post(url, headers=user_header, json=character_data)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.anyio
async def test_create_character_name_taken(client: AsyncClient) -> None:
    """Test character creation with name already taken: 400."""

    character_name = "Thrall"

    user = await factories.BaseUserFactory.create()
    user_header = test_utils.get_user_header(user.id)

    base_class = await factories.BaseClassFactory.create()
    await factories.CharacterFactory.create(
        character_name=character_name,
    )

    character_data = {
        "base_class_id": str(base_class.id),
        "gender": enums.Gender.male,
        "character_name": character_name,
    }

    response = await client.post(url, headers=user_header, json=character_data)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert "Character name already taken" in response.json()["detail"]


@pytest.mark.anyio
async def test_create_character_missing_data(client: AsyncClient) -> None:
    """Test character creation with missing data: 422."""

    user = await factories.BaseUserFactory.create()
    user_header = test_utils.get_user_header(user.id)

    character_data: dict[str, Any] = {}

    response = await client.post(url, headers=user_header, json=character_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.anyio
async def test_create_character_some_missing_data(client: AsyncClient) -> None:
    """Test character creation with missing data: 422."""

    user = await factories.BaseUserFactory.create()
    user_header = test_utils.get_user_header(user.id)

    base_class = await factories.BaseClassFactory.create()
    character_data = {
        "base_class_id": str(base_class.id),
        "gender": enums.Gender.male,
    }

    response = await client.post(url, headers=user_header, json=character_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.anyio
@pytest.mark.parametrize(
    "invalid_value",
    [
        1,  # int
        9.99,  # float
        True,  # boolean
        None,  # NoneType
        [1, 2, 3],  # list
        {"x": 1},  # dict
        (1, 2),  # tuple
    ],
)
async def test_create_character_invalid_data_type(
    client: AsyncClient, invalid_value: Any
) -> None:
    """Test character creation with invalid data types: 422."""

    user = await factories.BaseUserFactory.create()
    user_header = test_utils.get_user_header(user.id)

    base_class = await factories.BaseClassFactory.create()
    character_data = {
        "base_class_id": str(base_class.id),
        "gender": invalid_value,
        "character_name": "Arthas Menethil",
    }

    response = await client.post(url, headers=user_header, json=character_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.anyio
async def test_create_character_invalid_token(client: AsyncClient) -> None:
    """Test character creation with invalid token: 401."""

    user_header = {"Authorization": "Bearer invalid"}

    base_class = await factories.BaseClassFactory.create()
    character_data = {
        "base_class_id": str(base_class.id),
        "gender": enums.Gender.female,
        "character_name": "Sylvanas Windrunner",
    }

    response = await client.post(url, headers=user_header, json=character_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
async def test_create_character_no_token(client: AsyncClient) -> None:
    """Test character creation with no token: 401."""

    base_class = await factories.BaseClassFactory.create()
    character_data = {
        "base_class_id": str(base_class.id),
        "gender": enums.Gender.male,
        "character_name": "Vol'jin",
    }

    response = await client.post(url, json=character_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
