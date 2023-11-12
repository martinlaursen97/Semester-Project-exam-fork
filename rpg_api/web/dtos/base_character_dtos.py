from pydantic import BaseModel
from uuid import UUID
from rpg_api.core.dtos.base_schemas import OrmBasicModel

from rpg_api.enums import Gender
from rpg_api.web.dtos.base_class_dtos import BaseClassDTO


class BaseCharacterDTO(OrmBasicModel):
    """Base character DTO."""

    id: UUID
    base_class_id: UUID
    user_id: UUID
    gender: Gender
    character_name: str
    alive: bool
    level: int
    xp: int
    money: int


class BaseCharacterInputDTO(BaseModel):
    """Base character input DTO."""

    base_class_id: UUID
    user_id: UUID
    gender: Gender
    character_name: str
    alive: bool = True
    level: int = 1
    xp: int = 1
    money: int = 1


class BaseCharacterPartialInputDTO(BaseModel):
    """Base character partial input DTO."""

    base_class_id: UUID
    gender: Gender
    character_name: str


class BaseCharacterNestedWithClassDTO(BaseCharacterDTO):
    """Base character nested with class DTO."""

    id: UUID
    gender: Gender
    character_name: str
    alive: bool
    level: int
    xp: int
    money: int
    base_class: BaseClassDTO


class BaseCharacterUpdateDTO(BaseModel):
    """Base character update DTO."""

    gender: Gender | None = None
    character_name: str | None = None
    alive: bool | None = None
    level: int | None = None
    xp: int | None = None
    money: int | None = None
