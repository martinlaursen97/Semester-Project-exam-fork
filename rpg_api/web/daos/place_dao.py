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
from uuid import UUID, uuid4


class PlaceDAO(BaseSearchableDAO[Place, PlaceDTO, PlaceInputDTO, PlaceUpdateDTO]):
    """Class for accessing user table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        super().__init__(
            session=session,
            model=Place,
            base_dto=PlaceDTO,
        )

    async def create(self, input_dto: PlaceInputDTO) -> UUID:
        """Add single object to session and return the new object."""

        id = uuid4()

        try:
            self.session.add(Place(id=id, **input_dto.model_dump()))
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            raise e

        return id
