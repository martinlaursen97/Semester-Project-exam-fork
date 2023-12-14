from fastapi import APIRouter
from rpg_api.utils import dtos
from rpg_api.db.neo4j.dependencies import Neo4jSession
from rpg_api.web.daos.item_dao import NeoItemDAO

from datetime import datetime
router = APIRouter()


@router.post("/")
async def add_item(
    input_dto: dtos.NeoItemInputDTO, session: Neo4jSession
) -> dtos.DefaultCreatedResponse:
    dao = NeoItemDAO(session=session)
    id = await dao.create(input_dto=input_dto)

    return dtos.DefaultCreatedResponse(data=id)


@router.post("/character")
async def add_item_to_character() -> str:
    return "hello"
