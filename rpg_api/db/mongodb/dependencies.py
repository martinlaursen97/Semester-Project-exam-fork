from fastapi import Depends, Request
from typing import Annotated
from motor.core import AgnosticClient


def get_mongodb_client(
    request: Request,
) -> AgnosticClient:
    """
    Get mongodb client.

    :param request: request object
    """

    return request.app.state.mongodb_client


MongoClient = Annotated[AgnosticClient, Depends(get_mongodb_client)]
