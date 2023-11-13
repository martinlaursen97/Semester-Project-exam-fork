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
from fastapi.staticfiles import StaticFiles

from rpg_api.web.daos.base_class_dao import BaseClassDAO
from rpg_api.web.dtos.base_class_dtos import BaseClassInputDTO


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


async def _setup_startdata(app: FastAPI) -> None:  # pragma: no cover
    """Create startup data for the postgresql database."""

    session = app.state.db_session_factory()
    base_class_dao = BaseClassDAO(session=session)

    classes = ["Warrior", "Mage", "Shaman"]
    db_classes = await base_class_dao.filter()

    for class_name in classes:
        if not any([db_class.name == class_name for db_class in db_classes]):
            await base_class_dao.create(input_dto=BaseClassInputDTO(name=class_name))

    await session.commit()
    await session.close()


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
        await _setup_startdata(app)
        _setup_mongodb(app)
        await _setup_mongodb_startup_data(app)
        app.middleware_stack = app.build_middleware_stack()
        app.mount(
            "/static", StaticFiles(directory="rpg_api/templates/static"), name="static"
        )

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
