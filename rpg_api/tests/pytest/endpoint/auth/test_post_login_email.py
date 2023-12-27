import pytest
from httpx import AsyncClient
from fastapi import status
from rpg_api.db.postgres.factory import factories


URL = "/api/postgres/auth/login-email"


@pytest.mark.anyio
async def test_login_successful_and_access_token_in_response(
    client: AsyncClient,
) -> None:
    """Test successful login: 200."""

    # Create a user in the database
    user = await factories.BaseUserFactory.create()

    # Perform login
    response = await client.post(
        URL, json={"email": user.email, "password": "password"}
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()["data"]


@pytest.mark.anyio
async def test_login_incorrect_password(client: AsyncClient) -> None:
    """Test login incorrect password: 401."""

    # Create a user in the database
    user = await factories.BaseUserFactory.create()

    # Login request with incorrect password
    login_data = {"email": user.email, "password": "incorrect_password"}

    # Perform login
    response = await client.post(URL, json=login_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Wrong email or password" in response.json()["detail"]


@pytest.mark.anyio
async def test_login_incorrect_email(client: AsyncClient) -> None:
    """Test login incorrect email: 401."""

    # Create a user in the database
    await factories.BaseUserFactory.create()

    # Login request with incorrect email
    login_data = {"email": "some_email@email.com", "password": "password"}

    # Perform login
    response = await client.post(URL, json=login_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Wrong email or password" in response.json()["detail"]


@pytest.mark.anyio
@pytest.mark.parametrize(
    "invalid_email",
    [
        "plainaddress",
        "@missingusername.com",
        "missingdomain@.com",
        "missingatmark.com",
        "invalid@domain@domain.com",
        "invalid.com",
        "missingdot@domain",
        "two..dots@domain.com",
        "dot.@domain.com",
        "@domain.com",
        "user@.com",
        "user@.domain.com",
        "user@domain..com",
        "special@!$#%.comtest+email@example.com",
        ("longemail" * 10 + "@example.com"),  # Long email
        "test@ example.com",  # white space
    ],
)
async def test_login_invalid_email_format(
    invalid_email: str, client: AsyncClient
) -> None:
    """Test login with invalid email format: 422."""

    login_data = {"email": invalid_email, "password": "password"}

    # Login
    response = await client.post(URL, json=login_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.anyio
@pytest.mark.parametrize(
    "json_input", [{"password": "password"}, {"email": "mail@mail.com"}]
)
async def test_login_invalid_json_input(
    json_input: dict[str, str], client: AsyncClient
) -> None:
    """Test login invalid json input: 422."""

    # Login
    response = await client.post(URL, json=json_input)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.anyio
async def test_login_case_sensitivity(client: AsyncClient) -> None:
    """Test case sensitivity of email address. 401."""

    await factories.BaseUserFactory.create(email="TestEmail@example.com")
    response = await client.post(
        URL, json={"email": "testemail@example.com", "password": "password"}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
@pytest.mark.parametrize(
    "email",
    [
        "  test@example.com",
        "test@example.com  ",
        "  test@example.com  ",
    ],
)
async def test_login_email_extra_spaces(email: str, client: AsyncClient) -> None:
    """Test login with valid email having extra spaces. 200."""

    await factories.BaseUserFactory.create(email=email.strip())

    response = await client.post(URL, json={"email": email, "password": "password"})

    assert response.status_code == status.HTTP_200_OK


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
async def test_place_method_not_allowed(client: AsyncClient, method: str) -> None:
    """
    Test for method that are not allowed.
    """

    http_method = getattr(client, method)

    response = await http_method(URL)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
