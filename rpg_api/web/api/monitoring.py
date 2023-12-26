from fastapi import APIRouter, HTTPException
from typing import Any
from rpg_api.settings import settings
from rpg_api.db.mongo.dependencies import MongoClient
from rpg_api.db.neo4j.dependencies import Neo4jSession

monitoring_router = APIRouter()


@monitoring_router.get("/health")
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


@monitoring_router.get("/health-mongodb")
async def mongodb_check(mongo_client: MongoClient) -> Any:  # type: ignore
    """
    Checks the health of the mongodb.

    It returns 200 if the mongodb is healthy.
    """

    db = mongo_client["test_database"]
    db["test_collection"]

    return await db.command("ping")


@monitoring_router.get("/health-neo4j")
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
