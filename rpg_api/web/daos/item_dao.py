from fastapi import Depends
from rpg_api.core.daos.base_dao_neo4j import BaseNeo4jDAO
from rpg_api.utils.dtos import (
    NeoItemInputDTO,
    NeoItemDTO,
    NeoItemModel,
    NeoItemUpdateDTO,
    NeoItemCharacterEquipRelationshipDTO,
    NeoItemCharacterRelationshipDTO,
)
from neo4j import AsyncSession as AsyncNeoSession

from rpg_api.db.neo4j.dependencies import get_neo4j_session
from datetime import datetime
from rpg_api import exceptions as rpg_exc


class NeoItemDAO(BaseNeo4jDAO[NeoItemModel, NeoItemInputDTO, NeoItemUpdateDTO]):
    """Class for accessing character neo4j nodes."""

    def __init__(self, session: AsyncNeoSession = Depends(get_neo4j_session)):
        super().__init__(
            session=session,
            model=NeoItemModel,
        )

    async def add_item_to_character(
        self, rel_dto: NeoItemCharacterRelationshipDTO
    ) -> int | None:
        """
        Create a relationship of a specified type between two nodes.
        """

        rel_dto.relationship_props["created_at"] = datetime.now()

        create_rel_query = f"""
        MATCH (a:Character), (b:{self._label})
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
        print("wefwgw", record)
        if record:
            print(record)
            return record["r"].id
        return None

    async def equip_item_to_character(
        self, rel_dto: NeoItemCharacterEquipRelationshipDTO
    ) -> int | None:
        """
        Equip an item to a character, ensuring the item exists and has a 'HasItem' relationship.
        Also ensures only one 'EquippedAs...' relationship is active at a time.
        """
        rel_dto.relationship_props["created_at"] = datetime.now()

        equip_item_query = f"""
            MATCH (a:Character)-[:HasItem]->(b:{self._label})
            WHERE id(a) = $node1_id AND id(b) = $node2_id
            WITH a, b
            OPTIONAL MATCH (a)-[r]->()
            WHERE TYPE(r) STARTS WITH 'EquippedAs'
            DELETE r
            CREATE (a)-[new_r:{rel_dto.relationship_type}]->(b)
            SET new_r = $relationship_props
            RETURN new_r
            """

        result = await self.session.run(
            equip_item_query,
            node1_id=rel_dto.node1_id,
            node2_id=rel_dto.node2_id,
            relationship_props=rel_dto.relationship_props,
        )
        record = await result.single()

        if record:
            return record["new_r"].id
        return None

        result = await self.session.run(
            equip_item_query,
            node1_id=rel_dto.node1_id,
            node2_id=rel_dto.node2_id,
            relationship_props=rel_dto.relationship_props,
        )
        record = await result.single()

        if record:
            return record["new_r"].id
        return None

    async def get_user_items(self, user_id: int) -> list[NeoItemDTO]:
        """Get all character belonging to a user."""

        characters = []

        query = """
        MATCH (u:BaseUser)-[:HasA]->(c:Item)
        WHERE id(u) = $id
        RETURN c, id(c) as id
        """

        result = await self.session.run(query=query, id=user_id)

        for node in await result.data():
            character = NeoItemDTO.model_validate(node["c"])
            character.id = node["id"]
            characters.append(character)

        return characters

    async def get_item(self, item_id: int, user_id: int) -> NeoItemDTO:
        """Get character by id, belonging to a user."""

        query = """
        MATCH (u:BaseUser)-[:HasA]->(i:Item)
        WHERE id(u) = $user_id
        AND id(i) = $item_id
        RETURN i
        """

        result = await self.session.run(query=query, user_id=user_id, item_id=item_id)
        record = await result.single()

        if not record:
            raise rpg_exc.RowNotFoundError()

        character = NeoItemDTO.model_validate(record["i"])
        character.id = record["i"].id

        return character
