from typing import TypeVar
from rpg_api.core.daos.base_dao import BaseDAO, BaseDTO, InputDTO, UpdateDTO
from rpg_api.db.postgres.base import AbstractSearchableModel
from rpg_api.db.postgres.session import AsyncSessionWrapper as AsyncSession
import sqlalchemy as sa


Model = TypeVar("Model", bound=AbstractSearchableModel)


class BaseSearchableDAO(BaseDAO[Model, BaseDTO, InputDTO, UpdateDTO]):
    """Base class for accessing Scheduled Task tables."""

    def __init__(
        self, model: type[Model], base_dto: type[BaseDTO], session: AsyncSession
    ) -> None:
        super().__init__(model, base_dto, session)

    async def by_search(self, term: str) -> list[BaseDTO]:
        """Get by search term."""

        query = sa.select(self.model).filter(self.model.ts_vector.match(term))
        result = await self.session.execute(query)
        return [self.base_dto.model_validate(c) for c in result.scalars().all()]
