from typing import Generic, TypeVar
from uuid import UUID, uuid4

import sqlalchemy as sa
from pydantic import BaseModel

from rpg_api.db.postgres.base import Base
from rpg_api.db.postgres.session import (
    AsyncSessionWrapper as AsyncSession,
    ScalarResultWrapper,
)
from rpg_api import exceptions as rpg_exc
from sqlalchemy.orm.interfaces import LoaderOption
from typing import Any
import operator

Model = TypeVar("Model", bound=Base)
BaseDTO = TypeVar("BaseDTO", bound=BaseModel)
InputDTO = TypeVar("InputDTO", bound=BaseModel)
UpdateDTO = TypeVar("UpdateDTO", bound=BaseModel)


class BaseDAO(Generic[Model, BaseDTO, InputDTO, UpdateDTO]):  # noqa: WPS338
    """Generic class for accessing db."""

    def __init__(
        self,
        model: type[Model],
        base_dto: type[BaseDTO],
        session: AsyncSession,
    ):
        self.session = session
        self.model = model
        self.base_dto = base_dto
        self._tablename = self.model.__tablename__

    async def create(self, input_dto: InputDTO) -> UUID:
        """Add single object to session and return the new object."""

        id = uuid4()

        base = self.model(id=id, **input_dto.model_dump())
        self.session.add(base)
        await self.session.commit()
        return id

    async def update(self, id: UUID, update_dto: UpdateDTO) -> None:
        """Update an instance of the model in the database."""

        query = (
            sa.update(self.model)
            .where(self.model.id == id)
            .values(**update_dto.model_dump(exclude_none=True))  # type: ignore
        )
        await self.session.execute(query)
        await self.session.commit()

    async def _base_filter(
        self,
        order_by: str | None = None,
        loads: list[LoaderOption] | None = None,
        _limit_one: bool = False,
        **filter_params: Any,
    ) -> ScalarResultWrapper[Model]:
        """Get all instances of the model from the database."""

        query = sa.select(self.model)
        for key_name, value in filter_params.items():
            key, operation = split_key(key_name)
            if not hasattr(self.model, key):
                raise ValueError(f"Invalid filter key: {key}")
            if operation is not None:
                query = query.where(operation(getattr(self.model, key), value))
            elif isinstance(value, (list, set, tuple)):
                query = query.where(getattr(self.model, key).in_(value))
            else:
                query = query.where(getattr(self.model, key) == value)

        # Eager loading
        if loads is not None:
            for load in loads:
                query = query.options(load)

        # Limit one
        if _limit_one:
            query = query.limit(1)

        # Ordering
        query = query.order_by(getattr(self.model, order_by)) if order_by else query

        result = await self.session.execute(query)
        return result.scalars()

    async def filter(
        self,
        order_by: str | None = None,
        loads: list[LoaderOption] | None = None,
        **filter_params: Any,
    ) -> list[Model]:
        """Get all instances of the model by filter params."""

        res = await self._base_filter(
            order_by=order_by,
            loads=loads,
            **filter_params,
        )
        return res.all()

    async def filter_first(
        self,
        order_by: str | None = None,
        loads: list[LoaderOption] | None = None,
        **filter_params: Any,
    ) -> Model | None:
        """Get first instance of the model by filter params."""

        res = await self._base_filter(
            order_by=order_by,
            loads=loads,
            _limit_one=True,
            **filter_params,
        )
        return res.first()

    async def get_by_id(self, id: UUID) -> BaseDTO:
        """Get an instance of the model from the database by id."""

        query = sa.select(self.model).filter(self.model.id == id)
        instance = await self.session.execute(query)
        result = instance.scalars().first()

        if result is None:
            raise rpg_exc.RowNotFoundError(model_name=self.model.__name__)

        return self.base_dto.model_validate(result)


def split_key(key_name: str) -> tuple[str, Any | None]:
    """
    Split key into key and special operator.

    Returns the key and the operator if it exists else operator is None.
    """
    key_split = key_name.split("__")
    if not key_split:
        return key_name, None
    key = key_split[0]
    if len(key_split) == 1:
        return key, None
    special_key = key_split[1]
    return key, getattr(operator, special_key)
