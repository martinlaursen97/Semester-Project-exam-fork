from fastapi import APIRouter
from rpg_api.utils import dtos
from rpg_api.web.api.neo4j.auth.auth_dependencies import (
    GetCurrentUser,
    GetCharacterIfUserOwns,
)
from rpg_api.db.neo4j.dependencies import Neo4jSession
from rpg_api.web.daos.character_dao import NeoCharacterDAO
from rpg_api import exceptions as rpg_exceptions


router = APIRouter()


@router.get("")
async def characters_me(
    current_user: GetCurrentUser,
    session: Neo4jSession,
) -> dtos.DataListResponse[dtos.NeoCharacterModel]:
    """Get characters for logged in user."""
    dao = NeoCharacterDAO(session=session)

    chars = await dao.get_user_characters(user_id=int(current_user.id))

    return dtos.DataListResponse(data=chars)


@router.post("")
async def create_character(
    current_user: GetCurrentUser,
    input_dto: dtos.NeoCharacterInputDTO,
    session: Neo4jSession,
) -> dtos.EmptyDefaultResponse:
    """Create character."""

    dao = NeoCharacterDAO(session=session)

    character_id = await dao.create(input_dto=input_dto)

    await dao.create_relationship(
        rel_dto=dtos.NeoCharacterUserRelationshipDTO(
            node1_id=int(current_user.id),
            node2_id=character_id,
            relationship_type="HasA",
            relationship_props={},
        )
    )

    return dtos.EmptyDefaultResponse()


@router.patch("/{character_id}")
async def update_character(
    character: GetCharacterIfUserOwns,
    input_dto: dtos.NeoCharacterUpdateDTO,
    session: Neo4jSession,
) -> dtos.EmptyDefaultResponse:
    """Update character."""

    dao = NeoCharacterDAO(session=session)

    try:
        await dao.update(id=int(character.id), update_dto=input_dto)  # type: ignore
    except rpg_exceptions.RowNotFoundError:
        raise rpg_exceptions.HttpNotFound("Character not found.")

    return dtos.EmptyDefaultResponse()


@router.delete("/{character_id}")
async def delete_character(
    character: GetCharacterIfUserOwns,
    session: Neo4jSession,
) -> dtos.EmptyDefaultResponse:
    """Delete character if user owns."""

    dao = NeoCharacterDAO(session=session)

    try:
        await dao.delete_node_and_relationship(node_id=character.id)  # type: ignore
        return dtos.EmptyDefaultResponse()
    except rpg_exceptions.RowNotFoundError:
        raise rpg_exceptions.HttpNotFound("Character not found.")
