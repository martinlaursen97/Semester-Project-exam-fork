import pytest
from httpx import AsyncClient
from fastapi import status
from rpg_api.web.api.postgres.auth.token_store import token_store
from rpg_api.settings import settings
from rpg_api.db.postgres.factory import factories
from typing import Any
from rpg_api.web.api.postgres.auth import auth_utils as utils
from rpg_api.utils import dtos
from rpg_api.utils.daos import AllDAOs

url = "/api/postgres/characters"

def get_user_header(token: str) -> dict[str, Any]:
    """Return access token for given data."""
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.anyio
async def test_get_characters_empty_list(
    client: AsyncClient
) -> None:
    "Test get all characters with no characters in the database: 200."

    user = await factories.BaseUserFactory.create()

    # Create a token and store it in the token store
    token = utils.create_reset_password_token(
        data=dtos.TokenData(
            user_id=str(user.id),
        )
    )

    header = get_user_header(token)

    response = await client.get(url, headers=header)
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("data") == []


@pytest.mark.anyio
async def test_get_characters_populated_list(
    client: AsyncClient
) -> None:
    "Test get all characters with 1 character in the database: 200."

    user = await factories.BaseUserFactory.create()

    # Create a token and store it in the token store
    token = utils.create_reset_password_token(
        data=dtos.TokenData(
            user_id=str(user.id),
        )
    )

    header = get_user_header(token)

    character = await factories.CharacterFactory.create(user_id=user.id)

    response = await client.get(url, headers=header)
    print(character.__dict__)
    print(response.json())
    assert response.status_code == status.HTTP_200_OK
    #assert response.json().get("data")[0].get("id") == character.id


@pytest.mark.anyio
async def test_get_characters_invalid_token(
    client: AsyncClient
) -> None:
    "Test get all characters with invalid token: 401."

    header = get_user_header("invalid_token")

    response = await client.get(url, headers=header)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Invalid token" in response.json()["detail"]


@pytest.mark.anyio
async def test_get_characters_no_token(
    client: AsyncClient
) -> None:
    "Test get all characters with no token: 401."

    response = await client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Missing token." in response.json()["detail"]