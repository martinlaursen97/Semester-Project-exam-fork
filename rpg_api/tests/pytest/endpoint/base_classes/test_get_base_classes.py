import pytest
from httpx import AsyncClient
from fastapi import Response, status
from rpg_api.db.postgres.factory import factories
from rpg_api.tests.pytest import test_utils

url = "/api/postgres/base-classes"


@pytest.mark.anyio
async def test_get_base_classes_empty_list(client: AsyncClient) -> None:
    """Test get all base classes with 0 base classes in the database: 200."""

    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK

    response_data = test_utils.get_data(response)
    assert response_data == []
    assert len(response_data) == 0


@pytest.mark.anyio
async def test_get_base_classes_populated_list(client: AsyncClient) -> None:
    """Test get all base classes with 1 base class in the database: 200."""

    base_class = await factories.BaseClassFactory.create()

    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK

    response_data = test_utils.get_data(response)
    assert response_data[0]["id"] == str(base_class.id)
    assert response_data[0]["name"] == base_class.name


@pytest.mark.anyio
async def test_get_base_classes_populated_list_2(client: AsyncClient) -> None:
    """Test get all base classes with 2 base classes in the database: 200."""

    base_class1 = await factories.BaseClassFactory.create()
    base_class2 = await factories.BaseClassFactory.create()

    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK

    response_data = test_utils.get_data(response)
    assert response_data[0]["id"] == str(base_class1.id)
    assert response_data[0]["name"] == base_class1.name
    assert response_data[1]["id"] == str(base_class2.id)
    assert response_data[1]["name"] == base_class2.name
    assert len(response_data) == 2


@pytest.mark.anyio
@pytest.mark.parametrize(
    "method",
    [
        "post",
        "put",
        "delete",
        "patch",
        "options",
        "head",
    ],
)
async def test_base_classes_method_not_allowed(
    client: AsyncClient, method: str
) -> None:
    """
    Test that various HTTP methods are not
    allowed for the base classes endpoint: 405.
    """

    http_method = getattr(client, method)

    response: Response = await http_method(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
