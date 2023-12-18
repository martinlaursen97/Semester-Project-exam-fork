from typing import TypeVar, Generic
from neo4j import AsyncSession
from pydantic import BaseModel
from rpg_api.db.neo4j.base import Base
from rpg_api import exceptions as rpg_exc
from datetime import datetime
import neo4j.time

# Type variables for generic DAO
NodeModel = TypeVar("NodeModel", bound=Base)
InputDTO = TypeVar("InputDTO", bound=BaseModel)
UpdateDTO = TypeVar("UpdateDTO", bound=BaseModel)


class BaseNeo4jDAO(Generic[NodeModel, InputDTO, UpdateDTO]):
    """
    Generic class for Neo4j database access.
    """

    def __init__(
        self,
        model: type[NodeModel],
        session: AsyncSession,
    ):
        self.session = session
        self.model = model
        self._label = self.model.__label__

    async def create(self, input_dto: InputDTO) -> int:
        """
        Create a node based on input DTO.
        """
        now = datetime.now()
        props = input_dto.model_dump()
        print(now)
        props["created_at"] = now
        props["updated_at"] = now

        create_query = f"CREATE (n:{self._label} $props) RETURN n"
        result = await self.session.run(create_query, props=props)
        record = await result.single()

        if not record:
            raise rpg_exc.DatabaseError("hello")

        node = record["n"]
        return node.id

    async def get_by_id(self, node_id: int) -> NodeModel:
        """
        Get node by id.
        """

        query = "MATCH (n) WHERE id(n) = $id return n"
        result = await self.session.run(query=query, id=node_id)
        record = await result.single()

        if not record:
            raise rpg_exc.RowNotFoundError()

        node_data = dict(record["n"])

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

        # Validate and create the Pydantic model
        node = self.model.model_validate(node_data)
        node.id = record["n"].id
        return node

    async def get_by_property(self, input_dto: InputDTO) -> NodeModel | None:
        """
        Get a node based on properties from the input DTO.
        """

        query = f"MATCH (n:{self._label}) WHERE n += $props RETURN n"
        props = input_dto.model_dump()  # Convert DTO to a dictionary of properties
        result = await self.session.run(query, props=props)
        record = await result.single()

        if record:
            return self.model.model_validate(record["n"])
        return None

    async def update(self, id: int, update_dto: UpdateDTO) -> NodeModel | None:
        """
        Update a node based on DTO.
        """

        props_to_update = update_dto.model_dump()
        props_to_update["updated_at"] = datetime.now()
        props = {}

        # Iterate over each attribute in the DTO if it is not none then set
        for key, value in props_to_update.items():
            if value is not None:
                props[key] = value

        update_query = (
            f"MATCH (n:{self._label}) WHERE id(n) = $id SET n += $props return n"
        )
        result = await self.session.run(update_query, id=id, props=props)
        record = await result.single()

        if not record:
            raise rpg_exc.RowNotFoundError

        node_data = dict(record["n"])

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

        node = self.model.model_validate(node_data)
        node.id = id
        return node

    async def delete_node_and_relationship(self, node_id: int) -> None:
        """
        Delete a node by ID, this also deletes the relationships the node has.
        """

        delete_query = f"""
        MATCH (n:{self._label}) WHERE id(n) = $id 
        DETACH DELETE n 
        RETURN COUNT(n) as deleted_count"""

        result = await self.session.run(delete_query, id=node_id)
        delete_record = await result.single()

        if delete_record and delete_record["deleted_count"] == 0:
            raise rpg_exc.RowNotFoundError("No node was deleted")

    async def delete_node(self, node_id: int) -> None:
        """
        Delete a node by ID.
        If a node has a relationship,
        the node is not deleted and an exception is raised.
        """

        # Check for existing relationships
        check_query = f"""
        MATCH (n:{self._label})-[r]-() 
        WHERE id(n) = $id 
        RETURN COUNT(r) as rel_count"""

        result = await self.session.run(check_query, id=node_id)
        record = await result.single()

        if record and record["rel_count"] > 0:
            raise rpg_exc.HttpConflict("Node has relationships and cannot be deleted")

        # If no relationships, delete the node
        delete_query = f"""
        MATCH (n:{self._label}) 
        WHERE id(n) = $id 
        DETACH DELETE n 
        RETURN COUNT(n) as deleted_count"""

        result = await self.session.run(delete_query, id=node_id)
        delete_record = await result.single()

        if delete_record and delete_record["deleted_count"] == 0:
            raise rpg_exc.RowNotFoundError("No node was deleted")
