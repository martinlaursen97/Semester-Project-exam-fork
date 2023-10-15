from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi


async def create_async_motor_client() -> AsyncIOMotorClient:
    """
    Create async motor client.

    :return: async motor client.
    """
    return AsyncIOMotorClient(str(settings.mongodb_url))
