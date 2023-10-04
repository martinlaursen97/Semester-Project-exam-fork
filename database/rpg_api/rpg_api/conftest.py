from typing import Any, AsyncGenerator

import pytest
import sqlparse
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from rpg_api.db.dependencies import get_db_session
from rpg_api.db.utils import create_database, drop_database
from rpg_api.settings import settings
from rpg_api.web.application import get_app


async def run_sql_script(engine: AsyncEngine, script_path: str) -> None:
    """
    Run an SQL script against the provided engine.

    :param engine: The AsyncEngine to run the script against.
    :param script_path: The path to the SQL script file.
    """
    async with engine.begin() as conn:
        with open(script_path, "r") as file:
            sql_script = file.read()
            statements = sqlparse.split(sql_script)
            for statement in statements:
                if statement.strip():
                    await conn.execute(text(statement))


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """
    Backend for anyio pytest plugin.

    :return: backend name.
    """
    return "asyncio"


@pytest.fixture(scope="session")
async def _engine() -> AsyncGenerator[AsyncEngine, None]:
    """
    Create engine and databases.

    :yield: new engine.
    """
    from rpg_api.db.meta import meta  # noqa: WPS433
    from rpg_api.db.models import load_all_models  # noqa: WPS433

    load_all_models()

    await create_database()

    engine = create_async_engine(str(settings.db_url))
    async with engine.begin() as conn:
        await conn.run_sync(meta.create_all)

    from pathlib import Path

    # Get the current script path
    current_path = Path(__file__).resolve().parent

    #  SQL scripts
    script1_path = current_path.parent.parent / "db-scripts" / "1create_tables.sql"
    script2_path = current_path.parent.parent / "db-scripts" / "2create_test_data.sql"

    # # Execute SQL scripts
    await run_sql_script(engine, str(script1_path))
    await run_sql_script(engine, str(script2_path))

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
def fastapi_app(
    dbsession: AsyncSession,
) -> FastAPI:
    """
    Fixture for creating FastAPI app.

    :return: fastapi app with mocked dependencies.
    """
    application = get_app()
    application.dependency_overrides[get_db_session] = lambda: dbsession
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
