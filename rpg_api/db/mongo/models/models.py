from datetime import datetime
from uuid import UUID
from beanie import Indexed, Link, Document, PydanticObjectId
from rpg_api.db.mongo.models.base import MBase, MBaseMixins
from typing import List, Annotated
from pydantic import BaseModel, Field


from rpg_api.enums import Gender, MAttributeType, UserStatus


class MBaseUser(MBase):
    """BaseUser model for mongodb."""

    email: Annotated[str, Field(max_length=100), Indexed(unique=True)]
    password: Annotated[str, Field(max_length=255)]
    status: UserStatus = UserStatus.active
    characters: List[Link["MCharacter"]] = []
    friends: List[Link["MBaseUser"]] = []

    class Settings:
        name = "base_users"

    class Config:
        json_schema_extra = {
            "example": {
                "email": "example@gmail.org",
                "password": "password",
            }
        }

    @classmethod
    async def get_by_email(cls, email: str) -> "MBaseUser | None":
        """Get user by email."""
        return await cls.find_one({"email": email})


class EmbedLocation(BaseModel):
    """DTO for embedding location."""

    x: int
    y: int


class EmbedCharacterDetails(BaseModel):
    """DTO for embedding character details."""

    character_name: Annotated[str, Field(max_length=50), Indexed(unique=True)]
    level: Annotated[int, Indexed(unique=True)] = 1
    alive: bool = True
    xp: int = 0
    money: int = 0
    gender: Gender = Gender.male


class EmbedAttribute(BaseModel):
    """DTO for embedding attribute."""

    attribute: MAttributeType
    value: int = 1


class MCharacter(MBase):
    """Character model for mongodb."""

    user: Link["MBaseUser"]
    class_: Link["MClass"]
    character_attributes: list[EmbedAttribute]

    details: EmbedCharacterDetails
    location: EmbedLocation

    class Settings:
        name = "characters"

    class Config:
        json_schema_extra = {"example": {"character_name": "John", "level": 1}}


class MAbility(MBaseMixins):
    """Ability model for mongodb."""

    class Settings:
        name = "abilities"


class MClass(MBaseMixins):
    """Class model for mongodb."""

    abilities: List[Link["MAbility"]]

    class Settings:
        name = "classes"


class MPlace(MBaseMixins):
    """Place model for mongodb."""

    radius: int
    location: EmbedLocation | None = None

    class Settings:
        name = "places"
