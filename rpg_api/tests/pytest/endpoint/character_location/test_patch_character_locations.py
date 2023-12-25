import pytest
from httpx import AsyncClient
from fastapi import status
from rpg_api.db.postgres.factory import factories
from typing import Any
from rpg_api.web.api.postgres.auth import auth_utils as utils
from rpg_api.utils import dtos
import uuid

url = "/api/postgres/character-locations"


def get_user_header(token: str) -> dict[str, Any]:
    """Return access token for given data."""
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.anyio
@pytest.mark.parametrize(
    "x, y",
    [
        # Int32 boundaries
        (-2147483648, 0),
        (2147483647, 0),
        (0, -2147483648),
        (0, 2147483647),
        # Other values
        (-2147483647, 0),
        (2147483646, 0),
        (0, -2147483647),
        (0, 2147483646),
        (0, 0),
        (100, 100),
        (-100, -100),
    ],
)
async def test_patch_character_location_valid_boundaries(
    client: AsyncClient, x: int, y: int
) -> None:
    """ "Test updating character location with valid boundaries: 200."""

    user = await factories.BaseUserFactory.create()
    token = utils.create_access_token(data=dtos.TokenData(user_id=str(user.id)))
    header = get_user_header(token)

    character = await factories.CharacterFactory.create(user=user)
    # This ensures mypy knows that character_location is not None
    assert character.character_location is not None
    charLocation = {"x": x, "y": y}

    response = await client.patch(
        f"{url}/{character.id}", headers=header, json=charLocation
    )

    assert response.status_code == status.HTTP_200_OK
    assert character.character_location.x == x
    assert character.character_location.y == y


@pytest.mark.anyio
async def test_patch_character_location_missing_data(client: AsyncClient) -> None:
    """Test updating character location with one missing coordinate: 200."""

    user = await factories.BaseUserFactory.create()
    token = utils.create_access_token(data=dtos.TokenData(user_id=str(user.id)))
    header = get_user_header(token)

    character = await factories.CharacterFactory.create(user=user)
    # This ensures mypy knows that character_location is not None
    assert character.character_location is not None
    charLocation = {"x": 120}

    response = await client.patch(
        f"{url}/{character.id}", headers=header, json=charLocation
    )

    assert response.status_code == status.HTTP_200_OK
    assert character.character_location.x == 120
    assert character.character_location.y == 0


@pytest.mark.anyio
async def test_patch_character_location_invalid_data_type(client: AsyncClient) -> None:
    """Test updating character location with invalid data type and 0 valid ones: 422."""

    user = await factories.BaseUserFactory.create()
    token = utils.create_access_token(data=dtos.TokenData(user_id=str(user.id)))
    header = get_user_header(token)

    character = await factories.CharacterFactory.create(user=user)
    charLocation = {"x": "invalid"}

    response = await client.patch(
        f"{url}/{character.id}", headers=header, json=charLocation
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.anyio
async def test_patch_character_location_invalid_token(client: AsyncClient) -> None:
    """Test updating character location with invalid token: 401."""

    user = await factories.BaseUserFactory.create()
    header = get_user_header("invalid_token")

    character = await factories.CharacterFactory.create(user=user)
    charLocation = {"x": 0, "y": 0}

    response = await client.patch(
        f"{url}/{character.id}", headers=header, json=charLocation
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
async def test_patch_character_location_no_token(client: AsyncClient) -> None:
    """Test updating character location with no token: 401."""

    user = await factories.BaseUserFactory.create()

    character = await factories.CharacterFactory.create(user=user)
    charLocation = {"x": 0, "y": 0}

    response = await client.patch(f"{url}/{character.id}", json=charLocation)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
async def test_patch_character_location_invalid_character(client: AsyncClient) -> None:
    """Test updating character location with invalid character id: 404."""

    user = await factories.BaseUserFactory.create()
    token = utils.create_access_token(data=dtos.TokenData(user_id=str(user.id)))
    header = get_user_header(token)

    invalidId = uuid.uuid4()

    charLocation = {"x": 0, "y": 0}

    response = await client.patch(
        f"{url}/{invalidId}", headers=header, json=charLocation
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.anyio
async def test_patch_character_location_invalid_float(client: AsyncClient) -> None:
    """Test updating character location with a floating-point number: 422."""

    user = await factories.BaseUserFactory.create()
    token = utils.create_access_token(data=dtos.TokenData(user_id=str(user.id)))
    header = get_user_header(token)

    character = await factories.CharacterFactory.create(user=user)
    charLocation = {"x": 9.99}

    response = await client.patch(
        f"{url}/{character.id}", headers=header, json=charLocation
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.anyio
async def test_character_location_method_not_allowed_get(client: AsyncClient) -> None:
    """Test that GET method is not allowed for the character location endpoint."""

    user = await factories.BaseUserFactory.create()
    token = utils.create_access_token(data=dtos.TokenData(user_id=str(user.id)))
    header = get_user_header(token)

    character = await factories.CharacterFactory.create(user=user)

    response = await client.get(f"{url}/{character.id}", headers=header)

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.anyio
async def test_character_location_method_not_allowed_post(client: AsyncClient) -> None:
    """Test that POST method is not allowed for the character location endpoint."""

    user = await factories.BaseUserFactory.create()
    token = utils.create_access_token(data=dtos.TokenData(user_id=str(user.id)))
    header = get_user_header(token)

    character = await factories.CharacterFactory.create(user=user)

    response = await client.post(
        f"{url}/{character.id}", headers=header, json={"x": 10, "y": 20}
    )

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.anyio
async def test_character_location_method_not_allowed_put(client: AsyncClient) -> None:
    """Test that PUT method is not allowed for the character location endpoint."""

    user = await factories.BaseUserFactory.create()
    token = utils.create_access_token(data=dtos.TokenData(user_id=str(user.id)))
    header = get_user_header(token)

    character = await factories.CharacterFactory.create(user=user)
    response = await client.put(
        f"{url}/{character.id}", headers=header, json={"x": 10, "y": 20}
    )
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.anyio
async def test_character_location_method_not_allowed_delete(
    client: AsyncClient,
) -> None:
    """Test that DELETE method is not allowed for the character location endpoint."""

    user = await factories.BaseUserFactory.create()
    token = utils.create_access_token(data=dtos.TokenData(user_id=str(user.id)))
    header = get_user_header(token)

    character = await factories.CharacterFactory.create(user=user)

    response = await client.delete(f"{url}/{character.id}", headers=header)

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.anyio
async def test_character_location_method_not_allowed_options(
    client: AsyncClient,
) -> None:
    """Test that OPTIONS method is not allowed for the character location endpoint."""

    user = await factories.BaseUserFactory.create()
    token = utils.create_access_token(data=dtos.TokenData(user_id=str(user.id)))
    header = get_user_header(token)

    character = await factories.CharacterFactory.create(user=user)

    response = await client.options(f"{url}/{character.id}", headers=header)

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
