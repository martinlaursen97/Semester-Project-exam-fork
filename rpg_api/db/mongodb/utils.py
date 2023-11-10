from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticClient


def create_motor_client(url: str) -> AgnosticClient:
    """
    Create motor client.
    This does not create a connection to MongoDB, it just creates a client instance.
    Connections are created on demand, when performing operations.

    :return: motor client.
    """
    return AsyncIOMotorClient(url)
