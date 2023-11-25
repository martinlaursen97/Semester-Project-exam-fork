from collections.abc import AsyncGenerator
import random
import string
from typing import Any
from loguru import logger

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from rpg_api.web.api.auth import auth_utils as utils

from rpg_api.db.postgres.dependencies import get_db_session
from rpg_api.db.postgres.utils import (
    create_database,
    drop_database,
    create_extensions,
    run_scripts,
)
from rpg_api.db.postgres.session import AsyncSessionWrapper
from rpg_api.services.email_service.email_dependencies import (
    get_email_service,
)
from rpg_api.services.email_service.email_service import MockEmailService
from rpg_api.settings import settings
from rpg_api.web.application import get_app
from rpg_api.utils.daos import AllDAOs
from rpg_api.utils import dtos, models


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """
    Backend for anyio pytest plugin.

    :return: backend name.
    """
    return "asyncio"


@pytest.fixture(scope="session")
async def _engine() -> AsyncGenerator[AsyncEngine, None]:
    """Create engine and databases."""
    from rpg_api.db.postgres.meta import meta
    from rpg_api.db.postgres.models import load_all_models

    load_all_models()

    await create_database()
    await create_extensions()

    engine = create_async_engine(str(settings.db_url))
    async with engine.begin() as conn:
        await conn.run_sync(meta.create_all)

    try:
        await run_scripts(engine)
    except Exception as e:
        logger.info(e)

    try:
        yield engine
    finally:
        await engine.dispose()
        await drop_database()


@pytest.fixture
async def dbsession(
    _engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None]:
    """
    Get session to database.

    Fixture that returns a SQLAlchemy session with a SAVEPOINT, and the rollback to it
    after the test completes.

    :param _engine: current engine.
    :yields: async session.
    """
    connection = await _engine.connect()
    trans = await connection.begin()

    session_maker = async_sessionmaker(
        connection,
        expire_on_commit=False,
    )
    session = session_maker()

    try:
        yield session
    finally:
        await session.close()
        await trans.rollback()
        await connection.close()


@pytest.fixture
def daos(dbsession: AsyncSessionWrapper) -> AllDAOs:
    """Return DAOs for all tables in database."""
    return AllDAOs(dbsession)


@pytest.fixture
async def user_with_headers(
    daos: AllDAOs,
) -> tuple[models.BaseUser, dict[str, Any]]:
    """Create user with headers."""

    input_dto = dtos.BaseUserInputDTO(
        email=f"{''.join(random.choices(string.ascii_lowercase, k=10))}@example.com",
        password=utils.hash_password("password"),
    )

    new_id = await daos.base_user.create(input_dto)

    access_token = utils.get_headers(
        utils.create_access_token(
            data=dtos.TokenData(user_id=str(new_id)),
        )
    )

    db_user = await daos.base_user.filter_first(id=new_id)

    if db_user is None:
        raise Exception("User not found")

    return db_user, access_token


@pytest.fixture
async def mock_email_service() -> MockEmailService:
    """Get mock email service."""
    return MockEmailService()


@pytest.fixture
def fastapi_app(
    dbsession: AsyncSession,
    mock_email_service: MockEmailService,
) -> FastAPI:
    """
    Fixture for creating FastAPI app.

    :return: fastapi app with mocked dependencies.
    """
    application = get_app()
    application.dependency_overrides[get_db_session] = lambda: dbsession
    application.dependency_overrides[get_email_service] = lambda: mock_email_service
    return application  # noqa: WPS331


@pytest.fixture
async def client(
    fastapi_app: FastAPI,
    anyio_backend: Any,
) -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture that creates client for requesting server.

    :param fastapi_app: the application.
    :yield: client for the app.
    """
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


UserWithHeaders = tuple[models.BaseUser, dict[str, Any]]
