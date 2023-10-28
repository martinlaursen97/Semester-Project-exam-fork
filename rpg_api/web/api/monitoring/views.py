from fastapi import APIRouter
import motor.motor_asyncio
from typing import Any
from rpg_api.settings import settings

router = APIRouter()


@router.get("/health")
def health_check() -> Any:
    """
    Checks the health of a project.

    It returns 200 if the project is healthy.
    """

    return str(settings.db_url)


@router.get("/mongodb")
async def mongodb_check() -> Any:
    """
    Checks the health of the mongodb.

    It returns 200 if the mongodb is healthy.
    """
    mongodb_url = "mongodb://rpg_api:rpg_api@127.0.0.1:27017/?authMechanism=DEFAULT"
    client = motor.motor_asyncio.AsyncIOMotorClient(mongodb_url)
    db = client["rpg"]
    res = await db.command("ping")
    return res


# asd
# db = client["rpg"]
# res = await db.command("ping")
# return res
