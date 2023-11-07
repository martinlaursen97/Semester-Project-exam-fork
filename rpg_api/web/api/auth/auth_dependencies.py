from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer

from rpg_api import exceptions as exc
from rpg_api.utils import dtos
from rpg_api.utils.daos import AllDAOs
from rpg_api.web.apis.api.auth import auth_utils


class RpgHTTPBearer(HTTPBearer):
    """
    HTTPBearer with access token.
    Returns access token as str.
    """

    async def __call__(self, request: Request) -> str | None:  # type: ignore
        """Return str instead of object and 401 instead of 403."""
        try:
            obj = await super().__call__(request)
            return obj.credentials if obj else None
        except HTTPException:
            raise exc.HttpUnauthorized("Missing token.")


auth_scheme = RpgHTTPBearer()


def get_token(token: str = Depends(auth_scheme)) -> str:
    """Return access token as str."""
    return token


async def get_current_user(
    token: str = Depends(get_token), daos: AllDAOs = Depends()
) -> dtos.UserDTO:
    """Get current user from token data."""
    token_data = auth_utils.decode_token(token)

    try:
        return await daos.user.get_by_id(
            token_data.user_id,  # type: ignore
        )
    except exc.RowNotFoundError:
        raise exc.HttpNotFound("Decoded user not found.")
