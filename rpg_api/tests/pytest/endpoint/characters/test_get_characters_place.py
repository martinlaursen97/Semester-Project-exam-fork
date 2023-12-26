import pytest
from httpx import AsyncClient
from fastapi import status
from rpg_api.db.postgres.factory import factories
from rpg_api.tests.pytest import test_utils
from rpg_api.utils.daos import AllDAOs
from rpg_api.utils.dtos import CharacterLocationUpdateDTO
import uuid

url = "/api/postgres/characters/place"


@pytest.mark.anyio
async def test_get_character_place_wilderness(client: AsyncClient) -> None:
    """Test get character in an unnamed place (Wilderness): 200."""

    user = await factories.BaseUserFactory.create()
    header = test_utils.get_user_header(user.id)

    character = await factories.CharacterFactory.create(user=user)

    response = await client.get(f"{url}/{character.id}", headers=header)
    assert response.status_code == status.HTTP_200_OK

    response_data = test_utils.get_data(response)
    assert response_data["name"] == "Wilderness"


@pytest.mark.anyio
@pytest.mark.parametrize(
    "x_coordinate, y_coordinate, place_name",
    [
        (0, -432662, "Goldshire"),
        (-10, -35, "Orgrimmar"),
        (-888, 10, "Darnassus"),
        (245, 100, "Thunder Bluff"),
        (0, 0, "Elwynn Forest"),
    ],
)
async def test_get_character_place_named_place(
    client: AsyncClient,
    daos: AllDAOs,
    x_coordinate: int,
    y_coordinate: int,
    place_name: str,
) -> None:
    """Test get character in a named place: 200."""

    user = await factories.BaseUserFactory.create()
    header = test_utils.get_user_header(user.id)

    await factories.PlaceFactory.create(
        name=place_name, radius=0, x=x_coordinate, y=y_coordinate
    )
    character = await factories.CharacterFactory.create(user=user)
    character_location = await daos.character_location.get_by_id(
        character.character_location_id
    )
    update_data = CharacterLocationUpdateDTO(x=x_coordinate, y=y_coordinate)
    await daos.character_location.update(character_location.id, update_data)
    assert character.character_location.x == x_coordinate
    assert character.character_location.y == y_coordinate

    response = await client.get(f"{url}/{character.id}", headers=header)
    assert response.status_code == status.HTTP_200_OK

    response_data = test_utils.get_data(response)
    assert response_data["name"] == place_name


@pytest.mark.anyio
@pytest.mark.parametrize(
    "x_character, y_character, radius_place, x_place, y_place, name_place",
    [
        (2, -1, 3, 0, 0, "Goldshire"),
        (-10, -60, 10, -10, -50, "Stormwind"),
        (75, 50, 25, 75, 25, "Orgrimmar"),
        (1, -99, 100, 1, 1, "Thunder Bluff"),
    ],
)
async def test_get_character_place_named_place_radius_inside_boundary(
    client: AsyncClient,
    daos: AllDAOs,
    x_character: int,
    y_character: int,
    radius_place: int,
    x_place: int,
    y_place: int,
    name_place: str,
) -> None:
    """Test get character in the radius of a named place: 200."""

    user = await factories.BaseUserFactory.create()
    header = test_utils.get_user_header(user.id)

    await factories.PlaceFactory.create(
        name=name_place, radius=radius_place, x=x_place, y=y_place
    )
    character = await factories.CharacterFactory.create(user=user)
    character_location = await daos.character_location.get_by_id(
        character.character_location_id
    )
    update_data = CharacterLocationUpdateDTO(x=x_character, y=y_character)
    await daos.character_location.update(character_location.id, update_data)
    assert character.character_location.x == x_character
    assert character.character_location.y == y_character

    response = await client.get(f"{url}/{character.id}", headers=header)
    assert response.status_code == status.HTTP_200_OK

    response_data = test_utils.get_data(response)
    assert response_data["name"] == name_place


@pytest.mark.anyio
@pytest.mark.parametrize(
    "x_character, y_character, radius_place, x_place, y_place, name_place",
    [
        (2, -3, 3, 0, 0, "Goldshire"),
        (0, 4, 3, 0, 0, "Stormwind"),
        (-4, 0, 3, 0, 0, "Orgrimmar"),
        (49, 1, 50, 100, 1, "Thunder Bluff"),
    ],
)
async def test_get_character_place_named_place_outside_radius_boundary(
    client: AsyncClient,
    daos: AllDAOs,
    x_character: int,
    y_character: int,
    radius_place: int,
    x_place: int,
    y_place: int,
    name_place: str,
) -> None:
    """Test get character in an invalid EP boundary of the radius: 200."""

    user = await factories.BaseUserFactory.create()
    header = test_utils.get_user_header(user.id)

    await factories.PlaceFactory.create(
        name=name_place, radius=radius_place, x=x_place, y=y_place
    )
    character = await factories.CharacterFactory.create(user=user)
    character_location = await daos.character_location.get_by_id(
        character.character_location_id
    )
    update_data = CharacterLocationUpdateDTO(x=x_character, y=y_character)
    await daos.character_location.update(character_location.id, update_data)
    assert character.character_location.x == x_character
    assert character.character_location.y == y_character

    response = await client.get(f"{url}/{character.id}", headers=header)
    assert response.status_code == status.HTTP_200_OK

    response_data = test_utils.get_data(response)
    assert response_data["name"] == "Wilderness"


@pytest.mark.anyio
async def test_get_character_place_invalid_character(client: AsyncClient) -> None:
    """Test get character in a place with invalid character id: 404."""

    user = await factories.BaseUserFactory.create()
    header = test_utils.get_user_header(user.id)

    invalidId = uuid.uuid4()

    response = await client.get(f"{url}/{invalidId}", headers=header)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.anyio
async def test_get_character_place_invalid_token(client: AsyncClient) -> None:
    """Test get character in a place with invalid token: 401."""

    user = await factories.BaseUserFactory.create()
    header = {"Authorization": "Bearer invalid"}

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
    """Test that POST method is not allowed for the character place endpoint: 405."""

    character_id = uuid.uuid4()

    response = await client.post(f"{url}/{character_id}", json={"name": "NewPlace"})
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.anyio
async def test_character_place_method_not_allowed_put(client: AsyncClient) -> None:
    """Test that PUT method is not allowed for the character place endpoint: 405."""

    character_id = uuid.uuid4()

    response = await client.put(f"{url}/{character_id}", json={"name": "UpdatedPlace"})
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.anyio
async def test_character_place_method_not_allowed_delete(client: AsyncClient) -> None:
    """Test that DELETE method is not allowed for the character place endpoint: 405."""

    character_id = uuid.uuid4()

    response = await client.delete(f"{url}/{character_id}")
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.anyio
async def test_character_place_method_not_allowed_patch(client: AsyncClient) -> None:
    """Test that PATCH method is not allowed for the character place endpoint: 405."""

    character_id = uuid.uuid4()

    response = await client.patch(
        f"{url}/{character_id}", json={"name": "PatchedPlace"}
    )
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.anyio
async def test_character_place_method_not_allowed_options(client: AsyncClient) -> None:
    """Test that OPTIONS method is not allowed for the character place endpoint: 405."""

    character_id = uuid.uuid4()

    response = await client.options(f"{url}/{character_id}")
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.anyio
async def test_character_place_method_not_allowed_head(client: AsyncClient) -> None:
    """Test that HEAD method is not allowed for the character place endpoint: 405."""

    character_id = uuid.uuid4()

    response = await client.head(f"{url}/{character_id}")
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
