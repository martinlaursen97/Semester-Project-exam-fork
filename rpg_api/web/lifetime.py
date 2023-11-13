from collections.abc import Awaitable, Callable

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from rpg_api.db.mongodb.utils import create_motor_client
from beanie import init_beanie
from rpg_api.settings import settings
from rpg_api.db.postgres.meta import meta
from sqlalchemy.sql import text
from rpg_api.db.mongodb.models.base_user_model import MBaseUser
from loguru import logger
from neo4j import AsyncGraphDatabase


async def _setup_pg(app: FastAPI) -> None:  # pragma: no cover
    """
    Creates connection to the postgresql database.

    This function creates SQLAlchemy engine instance,
    session_factory for creating sessions
    and stores them in the application's state property.

    :param app: fastAPI application.
    """
    engine = create_async_engine(str(settings.db_url), echo=settings.db_echo)
    session_factory = async_sessionmaker(
        engine,
        expire_on_commit=False,
    )
    app.state.db_engine = engine
    app.state.db_session_factory = session_factory

    async with engine.begin() as conn:
        await conn.run_sync(meta.create_all)
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS citext"))

    # await run_scripts(engine)

    await engine.dispose()
    logger.info("Setting up database")


def _setup_mongodb(app: FastAPI) -> None:  # pragma: no cover
    """
    Creates connection to the mongodb database.

    :param app: fastAPI application.
    """

    app.state.mongodb_client = create_motor_client(str(settings.mongodb_url))


async def _setup_mongodb_startup_data(app: FastAPI) -> None:  # pragma: no cover
    """
    Creates connection to the mongodb database.

    :param app: fastAPI application.
    """

    await init_beanie(
        database=app.state.mongodb_client.base_user,
        document_models=[MBaseUser],  # type: ignore
    )


async def setup_neo4j(app: FastAPI) -> None:
    """
    Creates a connection to the Neo4j database.

    This function creates a Neo4j driver instance and stores it
    in the application's state property.
    """
    uri = "neo4j://rpg_api-neo4j:7687"
    app.state.neo4j_driver = AsyncGraphDatabase.driver(uri, auth=("neo4j", "password"))


def register_startup_event(
    app: FastAPI,
) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application startup.

    This function uses fastAPI app to store data
    in the state, such as db_engine.

    :param app: the fastAPI application.
    :return: function that actually performs actions.
    """

    @app.on_event("startup")
    async def _startup() -> None:  # noqa: WPS430
        app.middleware_stack = None
        await _setup_pg(app)
        _setup_mongodb(app)
        await setup_neo4j(app)
        await _setup_mongodb_startup_data(app)
        app.middleware_stack = app.build_middleware_stack()

    return _startup


def register_shutdown_event(
    app: FastAPI,
) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application's shutdown.

    :param app: fastAPI application.
    :return: function that actually performs actions.
    """

    @app.on_event("shutdown")
    async def _shutdown() -> None:  # noqa: WPS430
        await app.state.db_engine.dispose()
        await app.state.mongodb_client.close()

        pass  # noqa: WPS420

    return _shutdown
