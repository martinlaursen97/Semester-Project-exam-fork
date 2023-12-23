from fastapi import Depends, Request
from neo4j import AsyncDriver, AsyncSession
from typing import Annotated
from collections.abc import AsyncGenerator


async def get_neo4j_driver(request: Request) -> AsyncDriver:
    """
    Get Neo4j async driver.
    """
    return request.app.state.neo4j_driver


async def get_neo4j_session(
    driver: AsyncDriver = Depends(get_neo4j_driver),
) -> AsyncGenerator[AsyncSession, None]:
    """
    Get Neo4j async session.
    """
    
    async with driver.session() as session:
        tx = await session.begin_transaction()
        try:
            yield session
            await tx.commit()  # Commit the transaction if everything is fine
        except Exception as e:
            await tx.rollback()  # Rollback the transaction in case of an error
            raise e


Neo4jSession = Annotated[AsyncSession, Depends(get_neo4j_session)]
