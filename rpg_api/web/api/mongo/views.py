from fastapi import APIRouter
from typing import Any
from rpg_api.db.mongo.models.models import MCharacter
from rpg_api.db.mongo.dependencies import MongoClient

router = APIRouter()


@router.get("")
async def mongodb_check(mongo_client: MongoClient) -> Any:  # type: ignore
    """
    Checks the health of the mongodb.

    It returns 200 if the mongodb is healthy.
    """

    db = mongo_client["test_database"]
    db["test_collection"]

    MCharacter.find_all()

    return MCharacter.all()
    return await db.command("show dbs")
