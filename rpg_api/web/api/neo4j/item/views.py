from fastapi import APIRouter
from rpg_api.utils import dtos
from rpg_api.db.neo4j.dependencies import Neo4jSession
from rpg_api.web.daos.item_dao import NeoItemDAO
from rpg_api.web.api.neo4j.auth.auth_dependencies import (
    GetCurrentUser,
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
) -> str:
    """Add item to character."""
    dao = NeoItemDAO(session=session)

    await dao.add_item_to_character(input_dto)

    return "hello"


@router.post("/equip")
async def equip_item_to_character(
    input_dto: dtos.NeoItemCharacterEquipRelationshipDTO, session: Neo4jSession
) -> str:
    """Equip item to character."""

    dao = NeoItemDAO(session=session)

    await dao.equip_item_to_character(input_dto)

    return "hello"
