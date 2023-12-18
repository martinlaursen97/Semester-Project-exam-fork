from fastapi import Depends
from rpg_api.db.postgres.models.models import Character
from rpg_api.core.daos.base_dao import BaseDAO
from rpg_api.core.daos.base_dao_neo4j import BaseNeo4jDAO
from rpg_api.db.postgres.dependencies import get_db_session
from rpg_api.utils.dtos import (
    CharacterDTO,
    CharacterInputDTO,
    CharacterUpdateDTO,
    NeoCharacterModel,
    NeoCharacterInputDTO,
    NeoCharacterUpdateDTO,
    NeoCharacterUserRelationshipDTO,
    NeoCharacterDTO,
)
from rpg_api.db.postgres.session import AsyncSessionWrapper as AsyncSession
from uuid import UUID
import sqlalchemy as sa
from neo4j import AsyncSession as AsyncNeoSession

from rpg_api.db.neo4j.dependencies import get_neo4j_session
from datetime import datetime
from rpg_api import exceptions as rpg_exc
from rpg_api.utils.date_utils import convert_to_valid_time


class CharacterDAO(
    BaseDAO[
        Character,
        CharacterDTO,
        CharacterInputDTO,
        CharacterUpdateDTO,
    ]
):
    """Class for accessing user table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        super().__init__(
            session=session,
            model=Character,
            base_dto=CharacterDTO,
        )

    async def get_place(self, character_id: UUID) -> str:
        """Get character place."""

        # Call postgresql function `get_character_place`
        query = """
            SELECT * FROM public.get_character_place(:character_id :: uuid) as name;
        """

        result = await self.session.execute(
            sa.text(query), {"character_id": character_id}
        )

        return result.scalar_one()


class NeoCharacterDAO(
    BaseNeo4jDAO[NeoCharacterModel, NeoCharacterInputDTO, NeoCharacterUpdateDTO]
):
    """Class for accessing character neo4j nodes."""

    def __init__(self, session: AsyncNeoSession = Depends(get_neo4j_session)):
        super().__init__(
            session=session,
            model=NeoCharacterModel,
        )

    async def create_relationship(
        self, rel_dto: NeoCharacterUserRelationshipDTO
    ) -> int | None:
        """
        Create a relationship of a specified type between two nodes.
        """

        rel_dto.relationship_props["created_at"] = datetime.now()

        create_rel_query = f"""
        MATCH (a:BaseUser), (b:{self._label})
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
            return record["r"].id
        return None

    async def get_user_characters(self, user_id: int) -> list[NeoCharacterModel]:
        """Get all character belonging to a user."""

        characters = []

        query = """
        MATCH (u:BaseUser)-[:HasA]->(c:Character)
        WHERE id(u) = $id
        RETURN c, id(c) as id
        """

        result = await self.session.run(query=query, id=user_id)

        for node in await result.data():
            node_data = convert_to_valid_time(node["c"])
            character = self.model.model_validate(node_data)
            character.id = node["id"]
            characters.append(character)

        return characters

    async def get_character(self, character_id: int, user_id: int) -> NeoCharacterDTO:
        """Get character by id, belonging to a user."""

        query = """
        MATCH (u:BaseUser)-[:HasA]->(c:Character)
        WHERE id(u) = $user_id
        AND id(c) = $character_id
        RETURN c
        """

        result = await self.session.run(
            query=query, user_id=user_id, character_id=character_id
        )
        record = await result.single()

        if not record:
            raise rpg_exc.RowNotFoundError()

        node_data = convert_to_valid_time(dict(record["c"]))

        character = NeoCharacterDTO.model_validate(node_data)
        character.id = record["c"].id

        return character
