from typing import TypeVar, Generic, List
from neo4j import AsyncSession
from pydantic import BaseModel
from rpg_api.db.neo4j.base import Base

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
        create_query = f"CREATE (n:{self._label} $props) RETURN n"
        result = await self.session.run(create_query, props=input_dto.model_dump())
        record = await result.single()
        node = record["n"]
        return node.id

    async def get_by_property(
        self, property_name: str, property_value: str
    ) -> NodeModel:
        """
        Get a node by a specific property.
        """
        query = f"MATCH (n:{self._label}) WHERE n.{property_name} = $value RETURN n"
        result = await self.session.run(query, value=property_value)
        record = await result.single()
        if record:
            return self.model.model_validate(record["n"])
        return None

    async def update(self, node_id: int, update_dto: UpdateDTO) -> None:
        """
        Update a node based on DTO.
        """
        update_query = f"MATCH (n:{self._label}) WHERE id(n) = $id SET n += $props"
        await self.session.run(update_query, id=node_id, props=update_dto.model_dump())

    async def delete(self, node_id: int) -> None:
        """
        Delete a node by ID.
        """
        delete_query = f"MATCH (n:{self._label}) WHERE id(n) = $id DELETE n"
        await self.session.run(delete_query, id=node_id)
