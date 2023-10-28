from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticClient


def create_motor_client(url: str) -> AgnosticClient:
    """
    Create motor client.

    :return: motor client.
    """
    return AsyncIOMotorClient(url)
