from typing import Generic, TypeVar
from collections.abc import Awaitable, Callable, Iterable
from uuid import UUID, uuid4

import sqlalchemy as sa
from asyncpg import exceptions as asyncpg_exc
from pydantic import BaseModel
from sqlalchemy import exc as sa_exc

from rpg_api import exceptions as intree_exc
from rpg_api.db.base import Base
from rpg_api.db.session import AsyncSessionWrapper as AsyncSession
from rpg_api import exceptions as rpg_exc

Model = TypeVar("Model", bound=Base)
BaseDTO = TypeVar("BaseDTO", bound=BaseModel)
InputDTO = TypeVar("InputDTO", bound=BaseModel)
UpdateDTO = TypeVar("UpdateDTO", bound=BaseModel)
RunAndHandleOutput = TypeVar("RunAndHandleOutput")


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
        await self.flush()
        return id

    async def update(self, id: UUID | Iterable[UUID], update_dto: UpdateDTO) -> None:
        """Update object based on id or ids."""

        update_dict = update_dto.model_dump(exclude_unset=True)
        if not update_dict:
            raise intree_exc.HttpUnprocessableEntity("No input data to update.")

        ids: Iterable[UUID] = id if isinstance(id, Iterable) else [id]

        await self._run_and_handle_error(
            lambda: self.session.execute(
                statement=sa.update(self.model)
                .where(self.model.id.in_(ids))
                .values(**update_dict),
            ),
        )

    async def flush(self) -> None:
        """Flush session."""

        await self._run_and_handle_error(self.session.flush)

    async def _run_and_handle_error(
        self,
        function: Callable[[], Awaitable[RunAndHandleOutput]],
    ) -> RunAndHandleOutput:
        """Run function and handle errors."""

        code_to_exception = {
            asyncpg_exc.UniqueViolationError.sqlstate: intree_exc.UniqueConstraintError(
                "Error."
            ),
        }

        try:
            return await function()
        except sa_exc.DBAPIError as exc:
            await self.session.rollback()
            sqlstate = exc.orig.sqlstate  # type: ignore
            err = code_to_exception.get(sqlstate)
            if err is not None:
                raise err
            raise exc

    async def get_by_id(self, id: UUID) -> BaseDTO:
        """Get an instance of the model from the database by id."""

        query = sa.select(self.model).filter(self.model.id == id)
        instance = await self.session.execute(query)
        result = instance.scalars().first()

        if result is None:
            raise rpg_exc.RowNotFoundError(model_name=self.model.__name__)

        return self.base_dto.model_validate(result)
