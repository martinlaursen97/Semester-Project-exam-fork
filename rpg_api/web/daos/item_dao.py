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
import neo4j.time


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

        if record:
            return record["r"].id
        return None

    async def equip_item_to_character(
        self, rel_dto: NeoItemCharacterEquipRelationshipDTO
    ) -> int | None:
        """
        Equip an item to a character,
        ensuring the item exists and has a 'HasItem' relationship.
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

    async def get_character_items(
        self, character_id: int, equipped_only: bool
    ) -> list[NeoItemDTO]:
        """
        Get items on character, if equipped_only is true,
        only equipped items are returned.
        """

        if equipped_only:
            match_clause = (
                "MATCH (c:Character)-[r]->(i:Item) WHERE TYPE(r) "
                "STARTS WITH 'EquippedAs' AND id(c) = $character_id"
            )
        else:
            match_clause = (
                "MATCH (c:Character)-[:HasItem]->(i:Item) WHERE id(c) = $character_id"
            )

        query = f"""
        {match_clause}
        RETURN i, id(i) as id
        """
        items = []
        result = await self.session.run(query, character_id=character_id)

        for node in await result.data():
            node_data = dict(node["i"])

            # Convert Neo4j DateTime objects to Python datetime objects
            for key, value in node_data.items():
                if isinstance(value, neo4j.time.DateTime):
                    node_data[key] = datetime(
                        value.year,
                        value.month,
                        value.day,
                        value.hour,
                        value.minute,
                        value.second,
                        value.nanosecond // 1000,
                    )
            item = NeoItemDTO.model_validate(node_data)
            item.id = node["id"]
            items.append(item)

        return items
