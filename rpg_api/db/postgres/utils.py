from loguru import logger
from sqlalchemy import text
from sqlalchemy.engine import make_url


from rpg_api.settings import settings


import sqlparse

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
)


async def create_database() -> None:
    """Create a database."""
    db_url = make_url(str(settings.db_url.with_path("/postgres")))
    engine = create_async_engine(db_url, isolation_level="AUTOCOMMIT")

    async with engine.connect() as conn:
        database_existance = await conn.execute(
            text(
                f"SELECT 1 FROM pg_database WHERE datname='{settings.db_base}'",  # noqa: E501, S608
            ),
        )
        database_exists = database_existance.scalar() == 1

    if database_exists:
        await drop_database()

    async with engine.connect() as conn:  # noqa: WPS440
        await conn.execute(
            text(
                f'CREATE DATABASE "{settings.db_base}" ENCODING "utf8" TEMPLATE template1',  # noqa: E501
            ),
        )


async def drop_database() -> None:
    """Drop current database."""
    db_url = make_url(str(settings.db_url.with_path("/postgres")))
    engine = create_async_engine(db_url, isolation_level="AUTOCOMMIT")
    async with engine.connect() as conn:
        disc_users = (
            "SELECT pg_terminate_backend(pg_stat_activity.pid) "  # noqa: S608
            "FROM pg_stat_activity "
            f"WHERE pg_stat_activity.datname = '{settings.db_base}' "
            "AND pid <> pg_backend_pid();"
        )
        await conn.execute(text(disc_users))
        await conn.execute(text(f'DROP DATABASE "{settings.db_base}"'))


async def create_extensions() -> None:
    """Create extensions for current DB."""

    db_url = str(settings.db_url)
    engine = create_async_engine(db_url)
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS citext"))


async def run_sql_script(engine: AsyncEngine, script_path: str) -> None:
    """
    Run an SQL script against the provided engine.

    :param engine: The AsyncEngine to run the script against.
    :param script_path: The path to the SQL script file.
    """
    async with engine.begin() as conn:
        with open(script_path) as file:
            sql_script = file.read()
            statements = sqlparse.split(sql_script)
            for statement in statements:
                if statement.strip():
                    await conn.execute(text(statement))


async def run_scripts(engine: AsyncEngine) -> None:
    """Run all scripts."""

    # Temporary fix for the issue with the first run of the tests
    query = """
        SELECT EXISTS (
            SELECT 1 FROM base_user WHERE email = '1'
        )
    """

    async with engine.begin() as conn:
        result = await conn.execute(text(query))
        should_run = not result.scalar_one_or_none()
        logger.info(f"SQL Scripts Should run: {should_run}")

    if not should_run:
        return

    from pathlib import Path

    current_path = Path(__file__).resolve().parent.parent.parent.parent
    scripts_dir = current_path / "db-scripts"
    script1_path = scripts_dir / "0triggers.sql"

    await run_sql_script(engine, str(script1_path))

    if settings.environment == "dev":
        script2_path = scripts_dir / "test_data_insert.sql"
        await run_sql_script(engine, str(script2_path))
