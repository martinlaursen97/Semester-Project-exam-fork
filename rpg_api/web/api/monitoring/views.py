from fastapi import APIRouter, Depends, HTTPException
from typing import Any
from rpg_api.settings import settings
from rpg_api.db.mongodb.dependencies import MongoClient
from rpg_api.db.neo4j.dependencies import Neo4jSession
from rpg_api.web.dtos.neo4j_dtos import (
    PersonDTO,
    PersonUpdateDTO,
    PersonRelationshipDTO,
)
from rpg_api.web.daos.base_user_dao import PersonNeo4jDAO
from rpg_api.web.dtos.base_user_mongo import BaseUserInsert

router = APIRouter()


@router.get("/health")
def health_check() -> Any:
    """
    Checks the health of a project.

    It returns 200 if the project is healthy.
    """

    return (
        str(settings.db_url),
        str(settings.mongodb_url),
        "mongodb://rpg_api:rpg_api@127.0.0.1:27017/?authMechanism=DEFAULT",
    )


@router.get("/mongodb")
async def mongodb_check(mongo_client: MongoClient) -> Any:  # type: ignore
    """
    Checks the health of the mongodb.

    It returns 200 if the mongodb is healthy.
    """

    db = mongo_client["test_database"]
    db["test_collection"]

    return await db.command("ping")


@router.post("/mongodb-insert")
async def mongodb_insert(input_dto: BaseUserInsert, mongo_client: MongoClient) -> Any:  # type: ignore
    """
    Checks the health of the mongodb.

    It returns 200 if the mongodb is healthy.
    """

    db = mongo_client["test_database"]
    db["test_collection"]

    # insert a document
    await db.test_collection.insert_one(input_dto.model_dump())

    return await db.command("ping")


@router.get("/get-by-proptery")
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


@router.patch("node/{id}")
async def update_node(
    session: Neo4jSession, id: int, update_dto: PersonUpdateDTO
) -> dict[str, Any]:
    """Test view to update node by id."""
    person_dao = PersonNeo4jDAO(session=session)
    person = await person_dao.update(id=id, update_dto=update_dto)

    if person:
        return {"person": person.model_dump()}
    return {"message": "Person not found"}


@router.post("node/relationship")
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


@router.get("/neo4j")
async def neo4j_check(
    session: Neo4jSession,
) -> dict[Any, str]:
    """
    Checks the health of the Neo4j database.

    It returns 200 if the Neo4j database is healthy.
    """

    try:
        # Perform a simple read operation
        await session.run("MATCH (n) RETURN n LIMIT 1")
        return {"status": "Neo4j is operational"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
