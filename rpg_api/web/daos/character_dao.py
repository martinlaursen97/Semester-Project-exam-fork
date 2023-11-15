from fastapi import Depends
from rpg_api.db.postgres.models.models import Character
from rpg_api.core.daos.base_dao import BaseDAO
from rpg_api.db.postgres.dependencies import get_db_session
from rpg_api.utils.dtos import (
    CharacterDTO,
    CharacterInputDTO,
    CharacterUpdateDTO,
)
from rpg_api.db.postgres.session import AsyncSessionWrapper as AsyncSession


class CharacterDAO(
    BaseDAO[
        Character,
        CharacterDTO,
        CharacterInputDTO,
        CharacterUpdateDTO,
    ]
):
    """Class for accessing user table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        super().__init__(
            session=session,
            model=Character,
            base_dto=CharacterDTO,
        )
