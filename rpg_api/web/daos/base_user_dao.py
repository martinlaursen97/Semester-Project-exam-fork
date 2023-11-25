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
    PersonDTO,
    PersonModel,
    PersonUpdateDTO,
    PersonRelationshipDTO,
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


class PersonNeo4jDAO(BaseNeo4jDAO[PersonModel, PersonDTO, PersonUpdateDTO]):
    """Class for accessing user table."""

    def __init__(self, session: AsyncNeoSession = Depends(get_neo4j_session)):
        super().__init__(
            session=session,
            model=PersonModel,
        )

    async def create_relationship(
        self, rel_dto: PersonRelationshipDTO
    ) -> PersonRelationshipDTO | None:
        """
        Create a relationship of a specified type between two nodes.
        """
        create_rel_query = f"""
        MATCH (a:{self._label}), (b:{self._label})
        WHERE id(a) = $node1_id AND id(b) = $node2_id
        CREATE (a)-[r:{rel_dto.relationship_type}]->(b)
        SET r = $relationship_props
        RETURN r
        """
        result = await self.session.run(
            create_rel_query,
            node1_id=rel_dto.node1_id,
            node2_id=rel_dto.node2_id,
            relationship_props=rel_dto.relationship_props,
        )
        record = await result.single()

        if record:
            return record["r"]
        return None
