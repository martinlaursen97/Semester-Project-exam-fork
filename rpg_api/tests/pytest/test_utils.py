from rpg_api import constants
from rpg_api.utils import dtos
import uuid

from httpx import Response
from rpg_api.web.api.postgres.auth import auth_utils
from typing import Any


EMAIL_ADDITIONAL_LENGTH: int = len("@.com")
MAX_BEFORE_AT: int = 64
MAX_AFTER_AT: int = 63


def get_user_header(user_id: uuid.UUID | None = None) -> dict[str, str]:
    """Return access token for given data."""

    if user_id is not None and not isinstance(user_id, uuid.UUID):
        raise TypeError("user_id must be a uuid.UUID4")

    user_id = user_id or uuid.uuid4()
    token = dtos.TokenData(user_id=str(user_id))
    access_token = auth_utils.create_access_token(token)

    return {"Authorization": f"Bearer {access_token}"}


def get_data(response: Response) -> Any:
    """Get data from response."""
    return response.json()["data"]


def gen_email(before_at: int, after_at: int) -> str:
    """Generate an email of a given length before and after the @."""
    return f"{'a' * before_at}@{'b' * after_at}.com"


def gen_max_length_email(extra: int = 0) -> str:
    """Generate an email of maximum length."""
    extra += 1 if constants.MAX_LENGTH_EMAIL % 2 else 0
    return gen_email(
        constants.MAX_LENGTH_EMAIL // 2 + extra,
        constants.MAX_LENGTH_EMAIL // 2 - EMAIL_ADDITIONAL_LENGTH,
    )


def gen_min_length_email(extra: int = 0) -> str:
    """Generate an email of minimum length."""
    extra += 1 if constants.MIN_LENGTH_EMAIL % 2 else 0
    return gen_email(
        1,
        constants.MIN_LENGTH_EMAIL - 1 - EMAIL_ADDITIONAL_LENGTH + extra,
    )


def gen_string(length: int) -> str:
    """Generate a string of a given length."""
    return f"{'a' * length}"
