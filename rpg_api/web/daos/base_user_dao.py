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
    NeoBaseUserDTO,
    NeoBaseUserModel,
    NeoBaseUserUpdateDTO,
    NeoBaseUserRelationshipDTO,
    NeoBaseUserResponseLoginDTO,
)
from rpg_api.db.postgres.session import AsyncSessionWrapper as AsyncSession
from neo4j import AsyncSession as AsyncNeoSession
import sqlalchemy as sa
from datetime import datetime


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


class NeoBaseUserDAO(
    BaseNeo4jDAO[NeoBaseUserModel, NeoBaseUserDTO, NeoBaseUserUpdateDTO]
):
    """Class for accessing user table."""

    def __init__(self, session: AsyncNeoSession = Depends(get_neo4j_session)):
        super().__init__(
            session=session,
            model=NeoBaseUserModel,
        )

    async def get_by_email(self, email: str) -> NeoBaseUserResponseLoginDTO | None:
        """
        Get node by email.
        """

        query = f"MATCH (n:{self._label}) WHERE n.email = $email RETURN n"

        if self.session._transaction:
            result = await self.session._transaction.run(query=query, email=email)

        record = await result.single()

        if not record:
            return None

        # Validate and return the DTO
        return NeoBaseUserResponseLoginDTO(
            id=record["n"].id,
            email=record["n"].get("email"),
            password=record["n"].get("password"),
        )

    async def create_relationship(
        self, rel_dto: NeoBaseUserRelationshipDTO
    ) -> int | None:
        """
        Create a relationship of a specified type between two nodes.
        """
        rel_dto.relationship_props["created_at"] = datetime.now()

        create_rel_query = f"""
        MATCH (a:{self._label}), (b:{self._label})
        WHERE id(a) = $node1_id AND id(b) = $node2_id
        CREATE (a)-[r:{rel_dto.relationship_type}]->(b)
        SET r = $relationship_props
        RETURN r
        """

        if self.session._transaction:
            result = await self.session._transaction.run(
                create_rel_query,
                node1_id=rel_dto.node1_id,
                node2_id=rel_dto.node2_id,
                relationship_props=rel_dto.relationship_props,
            )
            
        record = await result.single()

        if record:
            return record["r"].id
        return None
