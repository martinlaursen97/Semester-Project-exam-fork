from fastapi import APIRouter
from rpg_api.utils import dtos
from rpg_api.db.neo4j.dependencies import Neo4jSession
from rpg_api.web.daos.item_dao import NeoItemDAO

from datetime import datetime
from pydantic import BaseModel

router = APIRouter()


@router.post("/")
async def add_item(
    input_dto: dtos.NeoItemInputDTO, session: Neo4jSession
) -> dtos.DefaultCreatedResponse:
    dao = NeoItemDAO(session=session)
    id = await dao.create(input_dto=input_dto)

    return dtos.DefaultCreatedResponse(data=id)


@router.post("/character")
async def add_item_to_character(
    input_dto: dtos.NeoItemCharacterRelationshipDTO, session: Neo4jSession
) -> str:
    dao = NeoItemDAO(session=session)

    await dao.add_item_to_character(input_dto)

    return "hello"


@router.post("/equip")
async def add_item_to_character(
    input_dto: dtos.NeoItemCharacterRelationshipDTO, session: Neo4jSession
) -> str:
    dao = NeoItemDAO(session=session)

    await dao.equip_item_to_character(input_dto)

    return "hello"
