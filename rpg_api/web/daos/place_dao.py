from fastapi import Depends
from rpg_api.core.daos.base_searchable_dao import BaseSearchableDAO
from rpg_api.db.postgres.models.models import Place
from rpg_api.db.postgres.dependencies import get_db_session
from rpg_api.utils.dtos import (
    PlaceDTO,
    PlaceInputDTO,
    PlaceUpdateDTO,
)
from rpg_api.db.postgres.session import AsyncSessionWrapper as AsyncSession

import sqlalchemy as sa


class PlaceDAO(BaseSearchableDAO[Place, PlaceDTO, PlaceInputDTO, PlaceUpdateDTO]):
    """Class for accessing user table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        super().__init__(
            session=session,
            model=Place,
            base_dto=PlaceDTO,
        )

    async def check_overlaps(self, x: int, y: int, radius: float) -> bool:
        """Check if new place overlaps with existing place."""

        query = """
            SELECT EXISTS (
                SELECT 1
                FROM place p
                WHERE public.calculate_distance(p.x, p.y, :x, :y) <= p.radius + :radius
            )
        """

        result = await self.session.execute(
            sa.text(query), {"x": x, "y": y, "radius": radius}
        )

        return bool(result.scalar_one())
