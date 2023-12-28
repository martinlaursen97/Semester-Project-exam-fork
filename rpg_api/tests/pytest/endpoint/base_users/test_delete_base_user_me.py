import pytest
from httpx import AsyncClient
from fastapi import status
from rpg_api.db.postgres.factory import factories
from rpg_api.tests.pytest import test_utils
from rpg_api.utils.daos import AllDAOs


url = "/api/postgres/base-users"


@pytest.mark.anyio
async def test_delete_current_user(client: AsyncClient, daos: AllDAOs) -> None:
    """Test deleting current user: 200."""

    user = await factories.BaseUserFactory.create()
    user_header = test_utils.get_user_header(user.id)

    response = await client.delete(url, headers=user_header)
    assert response.status_code == status.HTTP_200_OK

    db_user = await daos.base_user.filter_first(id=user.id)
    assert db_user is None


@pytest.mark.anyio
async def test_delete_current_user_not_found(client: AsyncClient) -> None:
    """Test deleting current user when user does not exist: 404."""

    user_header = test_utils.get_user_header()

    response = await client.delete(url, headers=user_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND
