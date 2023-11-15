from rpg_api.web.daos.base_user_dao import BaseUserDAO
from rpg_api.web.daos.character_dao import CharacterDAO
from rpg_api.web.daos.base_class_dao import BaseClassDAO
from rpg_api.web.daos.place_dao import PlaceDAO
from rpg_api.web.daos.character_location_dao import CharacterLocationDAO


from rpg_api.db.postgres.dependencies import get_db_session
from rpg_api.db.postgres.session import AsyncSessionWrapper as AsyncSession
from fastapi import Depends
from typing import Annotated


class AllDAOs:
    """Class for accessing all DAOs."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    @property
    def base_user(self) -> BaseUserDAO:
        """Base user DAO."""
        return BaseUserDAO(session=self.session)

    @property
    def character(self) -> CharacterDAO:
        """Character DAO."""
        return CharacterDAO(session=self.session)

    @property
    def base_class(self) -> BaseClassDAO:
        """Base class DAO."""
        return BaseClassDAO(session=self.session)

    @property
    def place(self) -> PlaceDAO:
        """Place DAO."""
        return PlaceDAO(session=self.session)

    @property
    def character_location(self) -> CharacterLocationDAO:
        """Character location DAO."""
        return CharacterLocationDAO(session=self.session)


GetDAOs = Annotated[AllDAOs, Depends(AllDAOs)]
