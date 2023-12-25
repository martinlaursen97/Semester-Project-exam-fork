import pytest
from httpx import AsyncClient
from fastapi import status
from rpg_api.db.postgres.factory import factories
from typing import Any
from rpg_api.web.api.postgres.auth import auth_utils as utils
from rpg_api.utils import dtos

url = "/api/postgres/characters"


def get_user_header(token: str) -> dict[str, Any]:
    """Return access token for given data."""
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.anyio
async def test_get_characters_empty_list(client: AsyncClient) -> None:
    "Test get all characters with 0 characters in the database: 200."

    user = await factories.BaseUserFactory.create()
    token = utils.create_access_token(data=dtos.TokenData(user_id=str(user.id)))
    header = get_user_header(token)

    response = await client.get(url, headers=header)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"] == []
    assert len(response.json()["data"]) == 0


@pytest.mark.anyio
async def test_get_characters_populated_list(client: AsyncClient) -> None:
    "Test get all characters with 1 character in the database: 200."

    user = await factories.BaseUserFactory.create()
    token = utils.create_access_token(data=dtos.TokenData(user_id=str(user.id)))
    header = get_user_header(token)

    character = await factories.CharacterFactory.create(user=user)
    # This ensures mypy knows that character_location is not None
    assert character.character_location is not None
    assert character.base_class is not None

    response = await client.get(url, headers=header)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"][0]["id"] == str(character.id)
    assert response.json()["data"][0]["gender"] == character.gender
    assert response.json()["data"][0]["character_name"] == character.character_name
    assert response.json()["data"][0]["alive"] == character.alive
    assert response.json()["data"][0]["level"] == character.level
    assert response.json()["data"][0]["xp"] == character.xp
    assert response.json()["data"][0]["money"] == character.money
    assert (
        response.json()["data"][0]["base_class"].get("name")
        == character.base_class.name
    )
    assert (
        response.json()["data"][0]["character_location"]["x"]
        == character.character_location.x
    )
    assert (
        response.json()["data"][0]["character_location"]["y"]
        == character.character_location.y
    )
    assert len(response.json()["data"]) == 1


@pytest.mark.anyio
async def test_get_characters_populated_list_2(client: AsyncClient) -> None:
    "Test get all characters with 2 characters in the database: 200."

    user = await factories.BaseUserFactory.create()
    token = utils.create_access_token(data=dtos.TokenData(user_id=str(user.id)))
    header = get_user_header(token)

    character1 = await factories.CharacterFactory.create(user=user)
    # This ensures mypy knows that character_location is not None
    assert character1.character_location is not None
    assert character1.base_class is not None
    character2 = await factories.CharacterFactory.create(user=user)
    # This ensures mypy knows that character_location is not None
    assert character2.character_location is not None
    assert character2.base_class is not None

    response = await client.get(url, headers=header)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"][0]["id"] == str(character1.id)
    assert response.json()["data"][0]["gender"] == character1.gender
    assert response.json()["data"][0]["character_name"] == character1.character_name
    assert response.json()["data"][0]["alive"] == character1.alive
    assert response.json()["data"][0]["level"] == character1.level
    assert response.json()["data"][0]["xp"] == character1.xp
    assert response.json()["data"][0]["money"] == character1.money
    assert (
        response.json()["data"][0]["base_class"].get("name")
        == character1.base_class.name
    )
    assert (
        response.json()["data"][0]["character_location"]["x"]
        == character1.character_location.x
    )
    assert (
        response.json()["data"][0]["character_location"]["y"]
        == character1.character_location.y
    )
    assert response.json()["data"][1]["id"] == str(character2.id)
    assert response.json()["data"][1]["gender"] == character2.gender
    assert response.json()["data"][1]["character_name"] == character2.character_name
    assert response.json()["data"][1]["alive"] == character2.alive
    assert response.json()["data"][1]["level"] == character2.level
    assert response.json()["data"][1]["xp"] == character2.xp
    assert response.json()["data"][1]["money"] == character2.money
    assert (
        response.json()["data"][1]["base_class"].get("name")
        == character2.base_class.name
    )
    assert (
        response.json()["data"][1]["character_location"]["x"]
        == character2.character_location.x
    )
    assert (
        response.json()["data"][1]["character_location"]["y"]
        == character2.character_location.y
    )
    assert len(response.json()["data"]) == 2


@pytest.mark.anyio
async def test_get_characters_invalid_token(client: AsyncClient) -> None:
    "Test get all characters with invalid token: 401."

    header = get_user_header("invalid_token")

    response = await client.get(url, headers=header)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
async def test_get_characters_no_token(client: AsyncClient) -> None:
    "Test get all characters with no token: 401."

    response = await client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
async def test_characters_method_not_allowed_put(client: AsyncClient) -> None:
    """Test that PUT method is not allowed for the base classes endpoint."""

    response = await client.put(url, json={"name": "Character"})

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.anyio
async def test_characters_method_not_allowed_delete(client: AsyncClient) -> None:
    """Test that DELETE method is not allowed for the base classes endpoint."""

    response = await client.delete(url)

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.anyio
async def test_characters_method_not_allowed_options(client: AsyncClient) -> None:
    """Test that OPTIONS method is not allowed for the base classes endpoint."""

    response = await client.options(url)

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.anyio
async def test_characters_method_not_allowed_patch(client: AsyncClient) -> None:
    """Test that PATCH method is not allowed for the base classes endpoint."""

    response = await client.patch(url, json={"name": "PatchedClass"})

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.anyio
async def test_characters_method_not_allowed_head(client: AsyncClient) -> None:
    """Test that HEAD method is not allowed for the base classes endpoint."""

    response = await client.head(url)

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
