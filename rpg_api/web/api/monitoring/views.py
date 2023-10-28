from fastapi import APIRouter
from typing import Any
from rpg_api.settings import settings
from rpg_api.db.mongodb.dependencies import MongoClient
from rpg_api.web.dtos.base_user import BaseUserInsert

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
async def mongodb_check(mongo_client: MongoClient) -> Any:
    """
    Checks the health of the mongodb.

    It returns 200 if the mongodb is healthy.
    """

    db = mongo_client["test_database"]
    db["test_collection"]

    return await db.command("ping")


@router.post("/mongodb-insert")
async def mongodb_insert(input_dto: BaseUserInsert, mongo_client: MongoClient) -> Any:
    """
    Checks the health of the mongodb.

    It returns 200 if the mongodb is healthy.
    """

    db = mongo_client["test_database"]
    db["test_collection"]

    # insert a document
    await db.test_collection.insert_one(input_dto.model_dump())

    return await db.command("ping")
