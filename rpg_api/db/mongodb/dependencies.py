from fastapi import Depends, Request
from typing import Annotated
from motor.core import AgnosticClient
from typing import Any


def get_mongodb_client(
    request: Request,
) -> Any:
    """
    Get mongodb client.

    :param request: request object
    """

    return request.app.state.mongodb_client


MongoClient = Annotated[AgnosticClient, Depends(get_mongodb_client)]  # type: ignore
