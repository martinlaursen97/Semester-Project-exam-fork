from typing import Any
import pytest
from httpx import AsyncClient
from fastapi import Response, status
from rpg_api.db.postgres.factory import factories
from rpg_api.tests.pytest import test_utils
from rpg_api.utils import models

url = "/api/postgres/characters"


def _assert_character_details(
    response_character: dict[str, Any], character: models.Character
) -> None:
    """Assert that the response character matches the character in the database."""
    assert response_character["id"] == str(character.id)
    assert response_character["gender"] == character.gender
    assert response_character["character_name"] == character.character_name
    assert response_character["alive"] == character.alive
    assert response_character["level"] == character.level
    assert response_character["xp"] == character.xp
    assert response_character["money"] == character.money

    if character.base_class:
        assert response_character["base_class"]["name"] == character.base_class.name

    if character.character_location:
        assert (
            response_character["character_location"]["x"]
            == character.character_location.x
        )
        assert (
            response_character["character_location"]["y"]
            == character.character_location.y
        )


@pytest.mark.anyio
@pytest.mark.parametrize(
    "create_num",
    [
        0,  # empty
        1,  # single
        2,  # multiple
    ],
)
async def test_get_characters(client: AsyncClient, create_num: int) -> None:
    """Test get all characters with various db states: 200."""

    user = await factories.BaseUserFactory.create()
    characters = await factories.CharacterFactory.create_batch(create_num, user=user)

    # Create a character for another user which should not be returned
    await factories.CharacterFactory.create()

    user_header = test_utils.get_user_header(user.id)

    response = await client.get(url, headers=user_header)
    assert response.status_code == status.HTTP_200_OK

    response_data = test_utils.get_data(response)
    assert len(response_data) == create_num

    for index, character in enumerate(characters):
        _assert_character_details(response_data[index], character)


@pytest.mark.anyio
async def test_get_characters_invalid_token(client: AsyncClient) -> None:
    """Test get all characters with invalid token: 401."""

    user_header = {"Authorization": "Bearer invalid"}

    response = await client.get(url, headers=user_header)
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

    response: Response = await http_method(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
