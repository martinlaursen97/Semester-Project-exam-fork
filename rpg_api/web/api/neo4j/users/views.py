from fastapi import APIRouter, Depends
from typing import Any
from rpg_api.db.neo4j.dependencies import Neo4jSession
from rpg_api.web.dtos.neo4j.base_user_dtos import (
    NeoBaseUserDTO,
    NeoBaseUserUpdateDTO,
    NeoBaseUserRelationshipDTO,
)
from rpg_api.web.daos.base_user_dao import NeoBaseUserDAO

router = APIRouter()


@router.get("/get-by-property")
async def get_by_property(
    session: Neo4jSession, input_dto: NeoBaseUserDTO = Depends()
) -> dict[str, Any]:
    """Test view for getting a property of a node."""

    person_dao = NeoBaseUserDAO(session=session)
    person = await person_dao.get_by_property(input_dto)

    if person:
        return {"person": person.model_dump()}
    return {"message": "Person not found"}


@router.get("/node/{id}")
async def get_by_id(session: Neo4jSession, id: int) -> dict[str, Any]:
    """Test view to get a node by id."""

    person_dao = NeoBaseUserDAO(session=session)
    try:
        person = await person_dao.get_by_id(id)
        return {"person": person.model_dump()}
    except Exception:
        return {"message": "Person not found"}


@router.patch("/node/{id}")
async def update_node(
    session: Neo4jSession, id: int, update_dto: NeoBaseUserUpdateDTO
) -> dict[str, Any]:
    """Test view to update node by id."""
    person_dao = NeoBaseUserDAO(session=session)
    person = await person_dao.update(id=id, update_dto=update_dto)

    if person:
        return {"person": person.model_dump()}
    return {"message": "Person not found"}


@router.post("/node/relationship")
async def create_relationship_person(
    session: Neo4jSession, relationship_dto: NeoBaseUserRelationshipDTO
) -> dict[str, Any]:
    """Test view to create relationship between two person nodes."""
    person_dao = NeoBaseUserDAO(session=session)
    person = await person_dao.create_relationship(rel_dto=relationship_dto)

    if person:
        return {"person": person}
    return {"message": "Person not found"}


@router.post("/add-node")
async def add_node(session: Neo4jSession, input_dto: NeoBaseUserDTO) -> dict[str, Any]:
    """Test view to add a node."""
    person_dao = NeoBaseUserDAO(session=session)
    result = await person_dao.create(input_dto=input_dto)

    return {"id": result}
