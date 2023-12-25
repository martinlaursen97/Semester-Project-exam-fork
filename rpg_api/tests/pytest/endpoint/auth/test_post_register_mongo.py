import pytest
from httpx import AsyncClient
from fastapi import status
from neo4j import AsyncSession

url = "/api/mongodb/auth/register"


@pytest.mark.anyio
async def test_register_user_success(
    client: AsyncClient,
    mongodb_test_db: AsyncSession,
) -> None:
    """Test registering a user with email and password: 200."""

    new_user_json = {"email": "test@mail.com", "password": "password"}

    response = await client.post(url, json=new_user_json)

    assert response.status_code == status.HTTP_201_CREATED
