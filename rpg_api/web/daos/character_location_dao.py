from fastapi import Depends
from rpg_api.db.postgres.models.models import CharacterLocation
from rpg_api.core.daos.base_dao import BaseDAO
from rpg_api.db.postgres.dependencies import get_db_session
from rpg_api.utils.dtos import (
    CharacterLocationDTO,
    CharacterLocationInputDTO,
    CharacterLocationUpdateDTO,
)
from rpg_api.db.postgres.session import AsyncSessionWrapper as AsyncSession


class CharacterLocationDAO(
    BaseDAO[
        CharacterLocation,
        CharacterLocationDTO,
        CharacterLocationInputDTO,
        CharacterLocationUpdateDTO,
    ]
):
    """Class for accessing user table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        super().__init__(
            session=session,
            model=CharacterLocation,
            base_dto=CharacterLocationDTO,
        )
