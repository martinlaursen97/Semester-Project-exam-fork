from fastapi import Depends
from rpg_api.db.postgres.models.models import BaseCharacter
from rpg_api.core.daos.base_dao import BaseDAO
from rpg_api.db.postgres.dependencies import get_db_session
from rpg_api.utils.dtos import (
    BaseCharacterDTO,
    BaseCharacterInputDTO,
    BaseCharacterUpdateDTO,
)
from rpg_api.db.postgres.session import AsyncSessionWrapper as AsyncSession


class BaseCharacterDAO(
    BaseDAO[
        BaseCharacter,
        BaseCharacterDTO,
        BaseCharacterInputDTO,
        BaseCharacterUpdateDTO,
    ]
):
    """Class for accessing user table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        super().__init__(
            session=session,
            model=BaseCharacter,
            base_dto=BaseCharacterDTO,
        )
