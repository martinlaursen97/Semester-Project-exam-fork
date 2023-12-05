from fastapi import APIRouter, Depends
from typing import Any
from rpg_api.db.neo4j.dependencies import Neo4jSession
from rpg_api.web.dtos.neo4j.neo4j_dtos import (
    PersonDTO,
    PersonUpdateDTO,
    PersonRelationshipDTO,
)
from rpg_api.web.daos.base_user_dao import PersonNeo4jDAO

router = APIRouter()


@router.get("/get-by-property")
async def get_by_property(
    session: Neo4jSession, input_dto: PersonDTO = Depends()
) -> dict[str, Any]:
    """Test view for getting a property of a node."""

    person_dao = PersonNeo4jDAO(session=session)
    person = await person_dao.get_by_property(input_dto)

    if person:
        return {"person": person.model_dump()}
    return {"message": "Person not found"}


@router.get("/node/{id}")
async def get_by_id(session: Neo4jSession, id: int) -> dict[str, Any]:
    """Test view to get a node by id."""

    person_dao = PersonNeo4jDAO(session=session)
    try:
        person = await person_dao.get_by_id(id)
        return {"person": person.model_dump()}
    except Exception:
        return {"message": "Person not found"}


@router.patch("/node/{id}")
async def update_node(
    session: Neo4jSession, id: int, update_dto: PersonUpdateDTO
) -> dict[str, Any]:
    """Test view to update node by id."""
    person_dao = PersonNeo4jDAO(session=session)
    person = await person_dao.update(id=id, update_dto=update_dto)

    if person:
        return {"person": person.model_dump()}
    return {"message": "Person not found"}


@router.post("/node/relationship")
async def create_relationship_person(
    session: Neo4jSession, relationship_dto: PersonRelationshipDTO
) -> dict[str, Any]:
    """Test view to create relationship between two person nodes."""
    person_dao = PersonNeo4jDAO(session=session)
    person = await person_dao.create_relationship(rel_dto=relationship_dto)
    print(person)
    if person:
        return {"person": person}
    return {"message": "Person not found"}


@router.post("/add-node")
async def add_node(session: Neo4jSession, input_dto: PersonDTO) -> dict[str, Any]:
    """Test view to add a node."""
    person_dao = PersonNeo4jDAO(session=session)
    result = await person_dao.create(input_dto=input_dto)

    return {"id": result}
