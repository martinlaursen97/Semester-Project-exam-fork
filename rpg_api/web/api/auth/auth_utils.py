from datetime import datetime, timedelta
from typing import Any

import jwt
from passlib.context import CryptContext

from rpg_api import exceptions
from rpg_api.settings import settings
from rpg_api.utils import dtos

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password."""

    return pwd_context.verify(plain_password, hashed_password)


def _encode_token(data: dtos.TokenData, expires_at: datetime) -> str:
    """Encode a token."""

    to_encode = data.model_dump()

    to_encode["exp"] = expires_at

    return jwt.encode(
        to_encode,
        settings.secret_key.get_secret_value(),
        algorithm=settings.algorithm,
    )


def create_access_token(data: dtos.TokenData) -> str:
    """Create an access token."""

    return _encode_token(
        data,
        datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes),
    )


def create_reset_password_token(data: dtos.TokenData) -> str:
    """Create an access token."""

    return _encode_token(
        data,
        datetime.utcnow()
        + timedelta(minutes=settings.reset_password_token_expire_minutes),
    )


def decode_token(token: str) -> dtos.TokenData:
    """Decode a token, returning the payload."""

    try:
        payload = jwt.decode(
            token,
            settings.secret_key.get_secret_value(),
            algorithms=[settings.algorithm],
        )
        return dtos.TokenData(**payload)

    except jwt.exceptions.PyJWTError:
        raise exceptions.HttpUnauthorized(message="Invalid token")


def get_headers(access_token: str) -> dict[str, Any]:
    """Get headers."""

    return {"Authorization": f"Bearer {access_token}"}
