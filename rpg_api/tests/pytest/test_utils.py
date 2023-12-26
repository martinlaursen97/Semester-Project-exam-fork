from rpg_api.utils import dtos
import uuid

from httpx import Response
from rpg_api.web.api.postgres.auth import auth_utils
from typing import Any


def get_user_header(user_id: uuid.UUID | None = None) -> dict[str, str]:
    """Return access token for given data."""

    user_id = user_id or uuid.uuid4()
    token = dtos.TokenData(user_id=str(user_id))
    access_token = auth_utils.create_access_token(token)

    return {"Authorization": f"Bearer {access_token}"}


def get_data(response: Response) -> Any:
    """Get data from response."""
    return response.json()["data"]
