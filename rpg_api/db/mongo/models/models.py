from beanie import Indexed, Link, Document
from rpg_api.db.mongo.models.base import MBase, MNameDescriptionMixin
from typing import List, Annotated
from pydantic import Field

from rpg_api.enums import Gender, UserStatus


class MBaseUser(MBase):
    """BaseUser model for mongodb."""

    email: Annotated[str, Field(max_length=100)]
    password: Annotated[str, Field(max_length=255)]
    status: UserStatus = UserStatus.active
    characters: List[Link["MCharacter"]] | None = None
    friends: List[Link["MBaseUser"]] | None = None

    class Settings:
        name = "base_users"


class MCharacter(Document):
    """Character model for mongodb."""

    user: Link["MBaseUser"]
    class_: Link["MClass"]
    character_attributes: List[Link["MAttribute"]] | None = None

    character_name: Annotated[str, Field(max_length=50)]
    level: Annotated[str, Indexed(unique=True)]
    alive: bool = True
    xp: int = 0
    money: int = 0
    gender: Gender = Gender.male
    x: int = 0
    y: int = 0

    class Settings:
        name = "characters"


class MAttribute(MBase, MNameDescriptionMixin):
    """Attribute model for mongodb."""

    value: int = 0

    class Settings:
        name = "attributes"


class MAbility(MBase, MNameDescriptionMixin):
    """Ability model for mongodb."""

    class Settings:
        name = "abilities"


class MClass(MBase, MNameDescriptionMixin):
    """Class model for mongodb."""

    abilities: List[Link["MAbility"]]

    class Settings:
        name = "classes"


class MPlace(MBase, MNameDescriptionMixin):
    """Place model for mongodb."""

    radius: int
    x: int
    y: int

    class Settings:
        name = "places"
