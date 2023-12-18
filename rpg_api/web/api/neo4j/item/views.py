from fastapi import APIRouter, Query
from rpg_api.utils import dtos
from rpg_api.db.neo4j.dependencies import Neo4jSession
from rpg_api.web.daos.item_dao import NeoItemDAO
from rpg_api.web.api.neo4j.auth.auth_dependencies import (
    GetCurrentUser,
    GetCharacterIfUserOwns,
)

router = APIRouter()


@router.post("/")
async def add_item(
    input_dto: dtos.NeoItemInputDTO, session: Neo4jSession
) -> dtos.DefaultCreatedResponse:
    """Create an item in the db."""
    dao = NeoItemDAO(session=session)
    id = await dao.create(input_dto=input_dto)

    return dtos.DefaultCreatedResponse(data=id)


@router.post("/character")
async def add_item_to_character(
    input_dto: dtos.NeoItemCharacterRelationshipDTO,
    session: Neo4jSession,
    current_user: GetCurrentUser,
) -> dtos.DefaultCreatedResponse:
    """Add item to character."""
    dao = NeoItemDAO(session=session)

    id = await dao.add_item_to_character(input_dto)

    return dtos.DefaultCreatedResponse(data=id)


@router.post("/equip")
async def equip_item_to_character(
    input_dto: dtos.NeoItemCharacterEquipRelationshipDTO, session: Neo4jSession
) -> dtos.DefaultCreatedResponse:
    """Equip item to character."""

    dao = NeoItemDAO(session=session)

    id = await dao.equip_item_to_character(input_dto)

    return dtos.DefaultCreatedResponse(data=id)


@router.get("/{character_id}/items")
async def get_character_items(
    character: GetCharacterIfUserOwns,
    session: Neo4jSession,
    equipped_only: bool = Query(
        default=False,
        description="Set to true to retrieve only equipped items,"
        " false to retrieve all items",
    ),
) -> dtos.DataListResponse[dtos.NeoItemDTO]:
    """Return items on character."""

    dao = NeoItemDAO(session=session)
    items = await dao.get_character_items(
        character_id=int(character.id), equipped_only=equipped_only  # type: ignore
    )
    return dtos.DataListResponse(data=items)
