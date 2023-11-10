from rpg_api.web.daos.base_user_dao import BaseUserDAO


from rpg_api.db.dependencies import get_db_session
from rpg_api.db.session import AsyncSessionWrapper as AsyncSession
from fastapi import Depends
from typing import Annotated


class AllDAOs:
    """Class for accessing all DAOs."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    @property
    def base_user(self) -> BaseUserDAO:
        return BaseUserDAO(session=self.session)


GetDAOs = Annotated[AllDAOs, Depends(AllDAOs)]
