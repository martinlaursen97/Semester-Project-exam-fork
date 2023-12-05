import pytest
from httpx import AsyncClient
from fastapi import status
from rpg_api.services.email_service.email_service import MockEmailService
from rpg_api.web.api.postgres.auth.token_store import token_store
from rpg_api.settings import settings
from rpg_api.db.postgres.factory import factories

url = "/api/postgres/auth/forgot-password"


@pytest.mark.anyio
@pytest.mark.parametrize(
    "email",
    # Valid equivalence classes
    [
        "user@example.com",  # Common email format
        "user@mail.example.com",  # Email with subdomain
        "user+name@domain.co",  # Email with a plus sign
        "user123@example.net",  # Email with numeric characters
    ],
)
async def test_forgot_password(
    email: str,
    client: AsyncClient,
    mock_email_service: MockEmailService,
) -> None:
    """Test post forgot password: 200."""

    user = await factories.BaseUserFactory.create(email=email)

    response = await client.post(url, json={"email": user.email})
    assert response.status_code == status.HTTP_200_OK

    assert len(mock_email_service.sent_emails) == 1
    sent_email = mock_email_service.sent_emails[0]

    assert sent_email.email == user.email
    assert sent_email.html is not None
    assert sent_email.subject == "Forgot password"
    assert sent_email.body == f"Hello {user.email}!"

    # Check that the token was stored
    token = token_store.pop(user_id=user.id)
    assert token is not None
    assert f"{settings.frontend_url}/reset-password?token={token}" in sent_email.html


@pytest.mark.anyio
async def test_forgot_password_user_not_found(
    client: AsyncClient,
    mock_email_service: MockEmailService,
) -> None:
    """Test post forgot password when user is not found: 200."""

    response = await client.post(url, json={"email": "notfound@example.com"})
    # We don't want to leak whether or not the user exists, so we return 200
    assert response.status_code == status.HTTP_200_OK

    # However, we don't send an email, nor do we store a token
    assert len(mock_email_service.sent_emails) == 0
    assert len(token_store.tokens) == 0


@pytest.mark.anyio
@pytest.mark.parametrize(
    "email",
    # Invalid equivalence classes
    [
        "invalid",  # Invalid format (missing @ symbol)
        "invalid@invalid",  # Invalid format (missing TLD)
        "invalid@invalid.",  # Invalid format (invalid TLD)
        "",  # Empty email"
        None,  # Null email
        0,  # Non-string input
        True,  # Non-string input
    ],
)
async def test_forgot_password_invalid_input(
    email: str,
    client: AsyncClient,
    mock_email_service: MockEmailService,
) -> None:
    """Test post forgot password with invalid input: 422."""

    response = await client.post(url, json={"email": email})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    assert len(mock_email_service.sent_emails) == 0
    assert len(token_store.tokens) == 0
