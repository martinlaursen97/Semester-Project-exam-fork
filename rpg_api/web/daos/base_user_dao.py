import sqlalchemy as sa
from fastapi import Depends
from rpg_api.db.postgres.models.models import BaseUser
from rpg_api.core.daos.base_dao import BaseDAO
from rpg_api.core.daos.base_dao_neo4j import BaseNeo4jDAO
from rpg_api.db.postgres.dependencies import get_db_session
from rpg_api.db.neo4j.dependencies import get_neo4j_session
from rpg_api.utils.dtos import (
    BaseUserDTO,
    BaseUserInputDTO,
    BaseUserUpdateDTO,
    PersonInputDTO,
    PersonModel,
    PersonUpdateDTO,
)
from rpg_api.db.postgres.session import AsyncSessionWrapper as AsyncSession
from neo4j import AsyncSession as AsyncNeoSession


class BaseUserDAO(BaseDAO[BaseUser, BaseUserDTO, BaseUserInputDTO, BaseUserUpdateDTO]):
    """Class for accessing user table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        super().__init__(
            session=session,
            model=BaseUser,
            base_dto=BaseUserDTO,
        )

    async def get_by_email(self, email: str) -> BaseUser | None:
        """Get user by email."""

        user = await self.session.execute(
            sa.select(BaseUser).filter(BaseUser.email == email),
        )
        return user.scalars().first()


class PersonNeo4jDAO(BaseNeo4jDAO[PersonModel, PersonInputDTO, PersonUpdateDTO]):
    """Class for accessing user table."""

    def __init__(self, session: AsyncNeoSession = Depends(get_neo4j_session)):
        super().__init__(
            session=session,
            model=PersonModel,
        )
