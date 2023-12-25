import pytest
from httpx import AsyncClient
from fastapi import status
from rpg_api.db.postgres.factory import factories
from typing import Any
from rpg_api.web.api.postgres.auth import auth_utils as utils
from rpg_api.utils import dtos
import uuid

url = "/api/postgres/characters"


def get_user_header(token: str) -> dict[str, Any]:
    """Return access token for given data."""
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.anyio
async def test_create_character_success(client: AsyncClient) -> None:
    """Test successful character creation: 201."""

    user = await factories.BaseUserFactory.create()
    token = utils.create_access_token(data=dtos.TokenData(user_id=str(user.id)))
    header = get_user_header(token)

    baseClass = await factories.BaseClassFactory.create()
    charData = {
        "base_class_id": str(baseClass.id),
        "gender": "male",
        "character_name": "Garrosh Hellscream",
    }

    response = await client.post(url, headers=header, json=charData)

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.anyio
async def test_create_character_missing_data(client: AsyncClient) -> None:
    """Test character creation with missing data: 422."""

    user = await factories.BaseUserFactory.create()
    token = utils.create_access_token(data=dtos.TokenData(user_id=str(user.id)))
    header = get_user_header(token)

    character_data = {
        "base_class_id": str(uuid.uuid4()),
    }

    response = await client.post(url, headers=header, json=character_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.anyio
async def test_create_character_invalid_data_type(client: AsyncClient) -> None:
    """Test character creation with invalid data types: 422."""

    user = await factories.BaseUserFactory.create()
    token = utils.create_access_token(data=dtos.TokenData(user_id=str(user.id)))
    header = get_user_header(token)

    baseClass = await factories.BaseClassFactory.create()
    charData = {
        "base_class_id": str(baseClass.id),
        "gender": 1,
        "character_name": "Arthas Menethil",
    }

    response = await client.post(url, headers=header, json=charData)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.anyio
async def test_create_character_invalid_token(client: AsyncClient) -> None:
    """Test character creation with invalid token: 401."""

    header = get_user_header("invalid_token")

    charData = {
        "base_class_id": "invalid_uuid",
        "gender": "female",
        "character_name": "Sylvanas Windrunner",
    }

    response = await client.post(url, headers=header, json=charData)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
async def test_create_character_no_token(client: AsyncClient) -> None:
    """Test character creation with no token: 401."""

    baseClass = await factories.BaseClassFactory.create()
    charData = {
        "base_class_id": str(baseClass.id),
        "gender": "male",
        "character_name": "Vol'jin",
    }

    response = await client.post(url, json=charData)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
