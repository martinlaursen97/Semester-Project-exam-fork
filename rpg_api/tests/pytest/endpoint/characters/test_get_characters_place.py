import pytest
from httpx import AsyncClient
from fastapi import status
from rpg_api.db.postgres.factory import factories
from typing import Any
from rpg_api.web.api.postgres.auth import auth_utils as utils
from rpg_api.utils import dtos
import uuid

url = "/api/postgres/characters/place"
updateUrl = "/api/postgres/character-locations"

def get_user_header(token: str) -> dict[str, Any]:
    """Return access token for given data."""
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.anyio
async def test_get_character_place_wilderness(client: AsyncClient) -> None:
    """Test get character in an unnamed place (Wilderness): 200."""

    user = await factories.BaseUserFactory.create()
    token = utils.create_access_token(data=dtos.TokenData(user_id=str(user.id)))
    header = get_user_header(token)

    character = await factories.CharacterFactory.create(user=user)

    response = await client.get(f"{url}/{character.id}", headers=header)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["name"] == "Wilderness"


@pytest.mark.anyio
async def test_get_character_place_named_place(client: AsyncClient) -> None:
    """Test get character in a named place: 200."""

    user = await factories.BaseUserFactory.create()
    token = utils.create_access_token(data=dtos.TokenData(user_id=str(user.id)))
    header = get_user_header(token)

    await factories.PlaceFactory.create(name="Goldshire", description="A small town", radius=10, x=25, y=-100)
    character = await factories.CharacterFactory.create(user=user)
    # Characters are always created at 0,0 so the location is updated after creation
    charLocation = {"x": 25, "y": -100}
    await client.patch(f"{updateUrl}/{character.id}", headers=header, json=charLocation)

    response = await client.get(f"{url}/{character.id}", headers=header)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["name"] == "Goldshire"


@pytest.mark.anyio
async def test_get_character_place_named_place_radius_inside_boundary(client: AsyncClient) -> None:
    """Test get character in the radius of a named place: 200."""

    user = await factories.BaseUserFactory.create()
    token = utils.create_access_token(data=dtos.TokenData(user_id=str(user.id)))
    header = get_user_header(token)

    await factories.PlaceFactory.create(name="Goldshire", description="A small town", radius=10, x=25, y=-100)
    character = await factories.CharacterFactory.create(user=user)
    # Characters are always created at 0,0 so the location is updated after creation
    charLocation = {"x": 25, "y": -90}
    await client.patch(f"{updateUrl}/{character.id}", headers=header, json=charLocation)

    response = await client.get(f"{url}/{character.id}", headers=header)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["name"] == "Goldshire"


@pytest.mark.anyio
async def test_get_character_place_named_place_outside_radius_boundary(client: AsyncClient) -> None:
    """Test get character in an invalid equivalence partitioning boundary of the radius: 200."""

    user = await factories.BaseUserFactory.create()
    token = utils.create_access_token(data=dtos.TokenData(user_id=str(user.id)))
    header = get_user_header(token)

    await factories.PlaceFactory.create(name="Goldshire", description="A small town", radius=10, x=25, y=-100)
    character = await factories.CharacterFactory.create(user=user)
    # Characters are always created at 0,0 so the location is updated after creation
    charLocation = {"x": 25, "y": -111}
    await client.patch(f"{updateUrl}/{character.id}", headers=header, json=charLocation)

    response = await client.get(f"{url}/{character.id}", headers=header)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["name"] == "Wilderness"


@pytest.mark.anyio
async def test_get_character_place_invalid_character(client: AsyncClient) -> None:
    """Test get character in a place with invalid character id: 404."""

    user = await factories.BaseUserFactory.create()
    token = utils.create_access_token(data=dtos.TokenData(user_id=str(user.id)))
    header = get_user_header(token)

    invalidId = uuid.uuid4()

    response = await client.get(f"{url}/{invalidId}", headers=header)

    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.anyio
async def test_get_character_place_invalid_token(client: AsyncClient) -> None:
    """Test get character in a place with invalid token: 401."""

    user = await factories.BaseUserFactory.create()
    header = get_user_header("invalid_token")

    character = await factories.CharacterFactory.create(user=user)

    response = await client.get(f"{url}/{character.id}", headers=header)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
async def test_get_character_place_no_token(client: AsyncClient) -> None:
    """Test get character in a place with no token: 401."""

    user = await factories.BaseUserFactory.create()

    character = await factories.CharacterFactory.create(user=user)

    response = await client.get(f"{url}/{character.id}")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
async def test_character_place_method_not_allowed_post(client: AsyncClient) -> None:
    """Test that POST method is not allowed for the character place endpoint."""

    character_id = uuid.uuid4()

    response = await client.post(f"{url}/{character_id}", json={"name": "NewPlace"})

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.anyio
async def test_character_place_method_not_allowed_put(client: AsyncClient) -> None:
    """Test that PUT method is not allowed for the character place endpoint."""

    character_id = uuid.uuid4()

    response = await client.put(f"{url}/{character_id}", json={"name": "UpdatedPlace"})

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.anyio
async def test_character_place_method_not_allowed_delete(client: AsyncClient) -> None:
    """Test that DELETE method is not allowed for the character place endpoint."""

    character_id = uuid.uuid4()

    response = await client.delete(f"{url}/{character_id}")

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.anyio
async def test_character_place_method_not_allowed_patch(client: AsyncClient) -> None:
    """Test that PATCH method is not allowed for the character place endpoint."""

    character_id = uuid.uuid4()

    response = await client.patch(f"{url}/{character_id}", json={"name": "PatchedPlace"})

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.anyio
async def test_character_place_method_not_allowed_options(client: AsyncClient) -> None:
    """Test that OPTIONS method is not allowed for the character place endpoint."""

    character_id = uuid.uuid4()

    response = await client.options(f"{url}/{character_id}")

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.anyio
async def test_character_place_method_not_allowed_head(client: AsyncClient) -> None:
    """Test that HEAD method is not allowed for the character place endpoint."""

    character_id = uuid.uuid4()

    response = await client.head(f"{url}/{character_id}")

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
