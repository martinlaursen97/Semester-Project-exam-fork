import pytest
from httpx import AsyncClient
from fastapi import status
from rpg_api.db.postgres.factory import factories
from rpg_api.tests.pytest import test_utils

url = "/api/postgres/characters"


@pytest.mark.anyio
async def test_get_characters_empty_list(client: AsyncClient) -> None:
    """Test get all characters with 0 characters in the database: 200."""

    user = await factories.BaseUserFactory.create()
    header = test_utils.get_user_header(user.id)

    response = await client.get(url, headers=header)
    assert response.status_code == status.HTTP_200_OK

    response_data = test_utils.get_data(response)
    assert response_data == []
    assert len(response_data) == 0


@pytest.mark.anyio
async def test_get_characters_one_character(client: AsyncClient) -> None:
    """Test get all characters with 1 character in the database: 200."""

    user = await factories.BaseUserFactory.create()
    header = test_utils.get_user_header(user.id)

    character = await factories.CharacterFactory.create(user=user)
    assert character.character_location is not None
    assert character.base_class is not None

    response = await client.get(url, headers=header)
    assert response.status_code == status.HTTP_200_OK

    response_data = test_utils.get_data(response)
    assert response_data[0]["id"] == str(character.id)
    assert response_data[0]["gender"] == character.gender
    assert response_data[0]["character_name"] == character.character_name
    assert response_data[0]["alive"] == character.alive
    assert response_data[0]["level"] == character.level
    assert response_data[0]["xp"] == character.xp
    assert response_data[0]["money"] == character.money
    assert response_data[0]["base_class"].get("name") == character.base_class.name
    assert response_data[0]["character_location"]["x"] == character.character_location.x
    assert response_data[0]["character_location"]["y"] == character.character_location.y
    assert len(response_data) == 1


@pytest.mark.anyio
async def test_get_characters_multiple_characters(client: AsyncClient) -> None:
    """
    Test get all characters with 3 characters in the database,
    but the user sending the request only has access to 2: 200.
    """

    user = await factories.BaseUserFactory.create()
    user_2 = await factories.BaseUserFactory.create()
    header = test_utils.get_user_header(user.id)

    user_characters = [
        await factories.CharacterFactory.create(user=user),
        await factories.CharacterFactory.create(user=user),
    ]
    user_2_characters = await factories.CharacterFactory.create(user=user_2)
    assert user_2_characters.character_location is not None
    assert user_2_characters.base_class is not None
    for character in user_characters:
        assert character.character_location is not None
        assert character.base_class is not None


    response = await client.get(url, headers=header)
    assert response.status_code == status.HTTP_200_OK

    response_data = test_utils.get_data(response)
    for index, character in enumerate(user_characters):
        assert response_data[index]["id"] == str(character.id)
        assert response_data[index]["gender"] == character.gender
        assert response_data[index]["character_name"] == character.character_name
        assert response_data[index]["alive"] == character.alive
        assert response_data[index]["level"] == character.level
        assert response_data[index]["xp"] == character.xp
        assert response_data[index]["money"] == character.money
        assert response_data[index]["base_class"].get("name") == character.base_class.name
        assert (
        response_data[index]["character_location"]["x"] == character.character_location.x
        )
        assert (
        response_data[index]["character_location"]["y"] == character.character_location.y
        )
    assert len(response_data) == 2


@pytest.mark.anyio
async def test_get_characters_invalid_token(client: AsyncClient) -> None:
    """Test get all characters with invalid token: 401."""

    header = {"Authorization": "Bearer invalid"}

    response = await client.get(url, headers=header)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
async def test_get_characters_no_token(client: AsyncClient) -> None:
    """Test get all characters with no token: 401."""

    response = await client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
@pytest.mark.parametrize(
    "method",
    [
        "put",
        "delete",
        "options",
        "patch",
        "head",
    ],
)
async def test_characters_method_not_allowed(client: AsyncClient, method: str) -> None:
    """
    Test that various HTTP methods are not
    allowed for the characters endpoint: 405.
    """

    http_method = getattr(client, method)

    response = await http_method(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
