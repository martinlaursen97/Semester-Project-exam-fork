import pytest
from httpx import AsyncClient
from fastapi import status
from rpg_api.db.postgres.factory import factories
from rpg_api.tests.pytest import test_utils
from rpg_api.tests.pytest.test_utils import get_data

url = "/api/postgres/places"


@pytest.mark.anyio  
@pytest.mark.parametrize("create_num", [0, 1, 2]  )  
async def test_get_all_places(client: AsyncClient, create_num: int) -> None:  
    """Test get all places: 200."""  

    # x = i is used to avoid overlapping places  
    places = [await factories.PlaceFactory.create(x=i) for i in range(create_num)]  

    response = await client.get(url)  
    assert response.status_code == status.HTTP_200_OK  

    response_data = get_data(response)  
    assert len(response_data) == create_num  

    for index, place in enumerate(places):  
        assert response_data[index]["id"] == str(place.id)  
        assert response_data[index]["name"] == place.name  
        assert response_data[index]["description"] == place.description  
        assert response_data[index]["x"] == place.x  
        assert response_data[index]["y"] == place.y  
        assert response_data[index]["radius"] == place.radius  


@pytest.mark.anyio
@pytest.mark.parametrize(
    "method",
    [
        "put",
        "delete",
        "patch",
        "options",
        "head",
    ],
)
async def test_place_method_not_allowed(
    client: AsyncClient, method: str
) -> None:
    """
    Test for method that are not allowed.
    """

    http_method = getattr(client, method)

    response = await http_method(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
