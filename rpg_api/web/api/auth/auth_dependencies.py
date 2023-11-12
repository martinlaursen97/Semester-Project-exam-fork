from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer

from rpg_api import exceptions as rpg_exc
from rpg_api.utils import dtos
from rpg_api.utils.daos import AllDAOs
from rpg_api.web.api.auth import auth_utils
from typing import Annotated


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
            raise rpg_exc.HttpUnauthorized("Missing token.")


auth_scheme = RpgHTTPBearer()


def get_token(token: str = Depends(auth_scheme)) -> str:
    """Return access token as str."""
    return token


async def get_current_user(
    token: str = Depends(get_token), daos: AllDAOs = Depends()
) -> dtos.BaseUserDTO:
    """Get current user from token data."""
    token_data = auth_utils.decode_token(token)

    try:
        return await daos.base_user.filter_first(
            id=token_data.user_id,  # type: ignore
        )
    except rpg_exc.RowNotFoundError:
        raise rpg_exc.HttpNotFound("Decoded user not found.")


GetCurrentUser = Annotated[dtos.BaseUserDTO, Depends(get_current_user)]
