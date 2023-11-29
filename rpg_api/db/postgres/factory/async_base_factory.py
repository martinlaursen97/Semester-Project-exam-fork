import asyncio
import inspect
from typing import Any, Generic, TypeVar

import factory

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.interfaces import LoaderOption

from rpg_api.db.postgres.base import Base

TModel = TypeVar("TModel", bound=Base)


class AsyncSQLAlchemyModelFactory(Generic[TModel], factory.Factory):
    """Base class for factories when using an async session."""

    session: AsyncSession
    _loads: list[LoaderOption] = []

    class Meta:
        abstract = True
        exclude = ("session",)

    @classmethod
    async def create(cls, *args: Any, **kwargs: Any) -> TModel:
        """Create an instance of a model."""

        instance = await super().create(*args, **kwargs)

        await cls.session.flush()
        await cls.session.refresh(instance)

        # query the new instance while eager loading relationships
        query = sa.select(type(instance)).where(type(instance).id == instance.id)
        for load in cls._loads:
            query = query.options(load)

        result = await cls.session.execute(query)

        return result.scalars().one()

    @classmethod
    async def create_batch(cls, size: int, *args: Any, **kwargs: Any) -> list[TModel]:
        """Create batch of instances."""
        return [await cls.create(*args, **kwargs) for _ in range(size)]

    @classmethod
    def _create(
        cls,
        model_class: type["AsyncSQLAlchemyModelFactory[TModel]"],
        *args: Any,
        **kwargs: Any,
    ) -> asyncio.Task["AsyncSQLAlchemyModelFactory[TModel]"]:
        """Create a model with given arguments and store it in the current session."""

        async def maker_coroutine() -> "AsyncSQLAlchemyModelFactory[TModel]":  # noqa: E501, WPS430
            """Coroutine that creates and saves model in DB."""
            for key, value in kwargs.items():
                # When using SubFactory, you'll have a Task in the corresponding kwarg
                # Await tasks to pass model instances instead, not the Task
                if inspect.isawaitable(value):
                    kwargs[key] = await value

            # add model to database
            return await cls._create_model(model_class, *args, **kwargs)

        # A Task can be awaited multiple times, unlike a coroutine.
        # Useful when a factory and a subfactory must share the same object.
        return asyncio.ensure_future(maker_coroutine())

    @classmethod
    async def _create_model(
        cls,
        model_class: type["AsyncSQLAlchemyModelFactory[TModel]"],
        *args: Any,
        **kwargs: Any,
    ) -> "AsyncSQLAlchemyModelFactory[TModel]":
        """Add a model in the database."""

        model = model_class(*args, **kwargs)
        cls.session.add(model)
        return model
