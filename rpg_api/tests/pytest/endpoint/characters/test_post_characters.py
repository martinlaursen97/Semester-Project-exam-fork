from typing import Any
import pytest
from httpx import AsyncClient
from fastapi import status
from rpg_api.db.postgres.factory import factories
from rpg_api.tests.pytest import test_utils

url = "/api/postgres/characters"


@pytest.mark.anyio
async def test_create_character_success(client: AsyncClient) -> None:
    """Test successful character creation: 201."""

    user = await factories.BaseUserFactory.create()
    header = test_utils.get_user_header(user.id)

    base_class = await factories.BaseClassFactory.create()
    character_data = {
        "base_class_id": str(base_class.id),
        "gender": "male",
        "character_name": "Garrosh Hellscream",
    }

    response = await client.post(url, headers=header, json=character_data)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.anyio
async def test_create_character_missing_data(client: AsyncClient) -> None:
    """Test character creation with missing data: 422."""

    user = await factories.BaseUserFactory.create()
    header = test_utils.get_user_header(user.id)

    character_data: dict[str, Any] = {}

    response = await client.post(url, headers=header, json=character_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.anyio
async def test_create_character_some_missing_data(client: AsyncClient) -> None:
    """Test character creation with missing data: 422."""

    user = await factories.BaseUserFactory.create()
    header = test_utils.get_user_header(user.id)

    base_class = await factories.BaseClassFactory.create()
    character_data = {
        "base_class_id": str(base_class.id),
        "gender": "male",
    }

    response = await client.post(url, headers=header, json=character_data)
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
    header = test_utils.get_user_header(user.id)

    base_class = await factories.BaseClassFactory.create()
    character_data = {
        "base_class_id": str(base_class.id),
        "gender": invalid_value,
        "character_name": "Arthas Menethil",
    }

    response = await client.post(url, headers=header, json=character_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.anyio
async def test_create_character_invalid_token(client: AsyncClient) -> None:
    """Test character creation with invalid token: 401."""

    header = {"Authorization": "Bearer invalid"}

    base_class = await factories.BaseClassFactory.create()
    character_data = {
        "base_class_id": str(base_class.id),
        "gender": "female",
        "character_name": "Sylvanas Windrunner",
    }

    response = await client.post(url, headers=header, json=character_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
async def test_create_character_no_token(client: AsyncClient) -> None:
    """Test character creation with no token: 401."""

    base_class = await factories.BaseClassFactory.create()
    character_data = {
        "base_class_id": str(base_class.id),
        "gender": "male",
        "character_name": "Vol'jin",
    }

    response = await client.post(url, json=character_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
