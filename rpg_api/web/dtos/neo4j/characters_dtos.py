from rpg_api.db.neo4j.base import Base, BaseRelationshipDTO
from rpg_api.enums import Gender, CharacterClass
from pydantic import BaseModel
from datetime import datetime


class NeoCharacterModel(Base):
    """Character DTO."""

    __label__ = "Character"
    id: int | None = None
    character_class: CharacterClass
    gender: Gender
    character_name: str
    alive: bool
    level: int
    xp: int
    money: int
    created_at: datetime | None = None
    updated_at: datetime | None = None


class NeoCharacterDTO(Base):
    """Character DTO."""

    id: int | None = None
    character_class: CharacterClass
    gender: Gender
    character_name: str
    alive: bool
    level: int
    xp: int
    money: int
    created_at: datetime | None = None
    updated_at: datetime | None = None


class NeoCharacterInputDTO(BaseModel):
    """Character input DTO."""

    gender: Gender
    character_class: CharacterClass
    character_name: str
    alive: bool = True
    level: int = 1
    xp: int = 1
    money: int = 1


class NeoCharacterUpdateDTO(BaseModel):
    """Character update DTO."""

    gender: Gender | None = None
    character_name: str | None = None
    alive: bool | None = None
    level: int | None = None
    xp: int | None = None
    money: int | None = None


class NeoCharacterUserRelationshipDTO(BaseRelationshipDTO):
    """User relation with a character, that validates the type of relationship given."""
