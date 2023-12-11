from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer

from rpg_api import exceptions
from rpg_api.utils import dtos
from rpg_api.web.api.postgres.auth import auth_utils
from typing import Annotated
from rpg_api.web.daos.base_user_dao import NeoBaseUserDAO
from rpg_api.db.neo4j.dependencies import Neo4jSession


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
            raise exceptions.HttpUnauthorized("Missing token.")


auth_scheme = RpgHTTPBearer()


def get_token(token: str = Depends(auth_scheme)) -> str:
    """Return access token as str."""
    return token


async def get_current_user(
    session: Neo4jSession,
    token: str = Depends(get_token),
) -> dtos.NeoBaseUserResponseDTO:
    """Get current user from token data."""
    token_data = auth_utils.decode_token(token)
    print(token_data)
    dao = NeoBaseUserDAO(session=session)
    try:
        return await dao.get_by_id(
            node_id=int(token_data.user_id),  # type: ignore
        )
    except exceptions.RowNotFoundError:
        raise exceptions.HttpNotFound("Decoded user not found.")


# async def get_character_if_user_owns(
#     character_id: UUID,
#     daos: GetDAOs,
#     current_user: dtos.BaseUserDTO = Depends(get_current_user),
# ) -> Character:
#     """Get character if current user owns it."""
#     character = await daos.character.filter_first(
#         id=character_id,
#         user_id=current_user.id,
#     )

#     if not character:
#         raise exceptions.HttpNotFound("Character not found.")

#     return character


# GetCharacterIfUserOwns = Annotated[Character, Depends(get_character_if_user_owns)]
GetCurrentUser = Annotated[dtos.BaseUserDTO, Depends(get_current_user)]
