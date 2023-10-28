from fastapi import Depends, Request
from typing import Annotated
from motor.core import AgnosticClient


async def get_mongodb_client(
    request: Request,
) -> AgnosticClient:
    """Get mongodb client."""

    return request.app.state.mongodb_client


MongoClient = Annotated[AgnosticClient, Depends(get_mongodb_client)]
