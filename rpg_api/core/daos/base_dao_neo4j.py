from typing import TypeVar, Generic
from neo4j import AsyncSession
from pydantic import BaseModel
from rpg_api.db.neo4j.base import Base
from rpg_api import exceptions as rpg_exc

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
        node = self.model.model_validate(record["n"])
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

        node = self.model.model_validate(record["n"])
        node.id = id
        return node

    async def delete(self, node_id: int) -> None:
        """
        Delete a node by ID.
        """
        delete_query = f"MATCH (n:{self._label}) WHERE id(n) = $id DELETE n"
        await self.session.run(delete_query, id=node_id)
