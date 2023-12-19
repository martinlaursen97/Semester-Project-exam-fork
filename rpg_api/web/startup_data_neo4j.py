from fastapi import FastAPI
from rpg_api.db.postgres.session import AsyncSessionWrapper
from rpg_api.web.api.postgres.auth import auth_utils

from rpg_api.web.daos.base_class_dao import BaseClassDAO
from rpg_api.web.daos.place_dao import PlaceDAO
from rpg_api.web.daos.base_user_dao import BaseUserDAO
from rpg_api.utils import dtos
import sqlalchemy as sa
from rpg_api.settings import settings
from neo4j import AsyncSession


async def create_startup_data_Neo4j(session: AsyncSession) -> None:  # pragma: no cover
    """Initializes the db with roles, classes, places, and users for the app."""

    await setup_indexes(session)


async def setup_indexes(session: AsyncSession) -> None:
    """Create indexes using the neo4j session"""

    index_creation_queries = [
        "CREATE INDEX baseUserEmailIndex IF NOT EXISTS FOR (n:BaseUser) ON (n.email);",
        "CREATE INDEX characterNameIndex IF NOT EXISTS FOR (n:Character) ON (n.name);",
        "CREATE INDEX ItemNameIndex IF NOT EXISTS FOR (n:Item) ON (n.name);",
    ]
    for query in index_creation_queries:
        await session.run(query)
