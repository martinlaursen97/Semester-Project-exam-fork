from fastapi import Depends, Request
from neo4j import AsyncDriver, AsyncSession
from typing import Annotated


async def get_neo4j_driver(request: Request) -> AsyncDriver:
    """
    Get Neo4j async driver.
    """
    return request.app.state.neo4j_driver


async def get_neo4j_session(
    driver: AsyncDriver = Depends(get_neo4j_driver),
) -> AsyncSession:
    """
    Get Neo4j async session.
    """
    session = driver.session()
    try:
        yield session
    finally:
        await session.close()


Neo4jSession = Annotated[AsyncSession, Depends(get_neo4j_session)]
