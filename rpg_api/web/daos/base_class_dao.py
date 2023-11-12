from fastapi import Depends
from rpg_api.db.postgres.models.models import BaseClass
from rpg_api.core.daos.base_dao import BaseDAO
from rpg_api.db.postgres.dependencies import get_db_session
from rpg_api.utils.dtos import (
    BaseClassDTO,
    BaseClassInputDTO,
    BaseClassUpdateDTO,
)
from rpg_api.db.postgres.session import AsyncSessionWrapper as AsyncSession


class BaseClassDAO(
    BaseDAO[
        BaseClass,
        BaseClassDTO,
        BaseClassInputDTO,
        BaseClassUpdateDTO,
    ]
):
    """Class for accessing user table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        super().__init__(
            session=session,
            model=BaseClass,
            base_dto=BaseClassDTO,
        )
