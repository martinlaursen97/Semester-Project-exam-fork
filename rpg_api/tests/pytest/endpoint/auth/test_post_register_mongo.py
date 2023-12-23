import pytest
from httpx import AsyncClient
from fastapi import status
from neo4j import AsyncSession

url = "/api/mongodb/auth/register"


@pytest.mark.anyio
async def test_register_success(
    client: AsyncClient,
    mongodb_test_db: AsyncSession,
) -> None:
    """Test reset password: 200. """

    new_user_json = {"email": "test@mail.com", "password": "password"}

    response = await client.post(url, json=new_user_json)
    print(response.__dict__)
    assert response.status_code == status.HTTP_201_CREATED
