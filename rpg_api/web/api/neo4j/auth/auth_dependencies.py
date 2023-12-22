from fastapi import Depends

from rpg_api import exceptions as rpg_exceptions
from rpg_api.utils import dtos
from rpg_api.web.api.postgres.auth import auth_utils
from typing import Annotated
from rpg_api.web.daos.base_user_dao import NeoBaseUserDAO
from rpg_api.web.daos.character_dao import NeoCharacterDAO
from rpg_api.db.neo4j.dependencies import Neo4jSession
from rpg_api.web.api.postgres.auth.auth_dependencies import get_token


async def get_current_user(
    session: Neo4jSession,
    token: str = Depends(get_token),
) -> dtos.NeoBaseUserResponseDTO:
    """Get current user from token data."""

    token_data = auth_utils.decode_token(token)
    dao = NeoBaseUserDAO(session=session)
    try:
        return await dao.get_by_id(
            node_id=int(token_data.user_id),  # type: ignore
        )
    except rpg_exceptions.RowNotFoundError:
        raise rpg_exceptions.HttpNotFound("Decoded user not found.")


async def get_character_if_user_owns(
    character_id: int,
    session: Neo4jSession,
    current_user: dtos.NeoBaseUserResponseDTO = Depends(get_current_user),
) -> dtos.NeoCharacterDTO:
    """Get character if current user owns it."""
    dao = NeoCharacterDAO(session=session)

    try:
        character = await dao.get_character(
            character_id=character_id,
            user_id=int(current_user.id),
        )
        return character
    except rpg_exceptions.RowNotFoundError:
        raise rpg_exceptions.HttpNotFound("Character not found.")


GetCharacterIfUserOwns = Annotated[
    dtos.NeoCharacterDTO, Depends(get_character_if_user_owns)
]
GetCurrentUser = Annotated[dtos.BaseUserDTO, Depends(get_current_user)]
