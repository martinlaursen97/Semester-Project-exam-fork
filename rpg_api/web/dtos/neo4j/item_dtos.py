from rpg_api.db.neo4j.base import Base, BaseRelationshipDTO
from rpg_api import enums
from datetime import datetime
from pydantic import BaseModel, validator
from typing import Any


class NeoItemModel(Base):
    """Model for items."""

    __label__ = "Item"

    id: int | None = None
    name: str
    description: str
    item_type: enums.ItemType
    stamina: int
    agility: int
    intelligence: int
    crit: int
    created_at: datetime | None = None
    updated_at: datetime | None = None


class NeoItemDTO(Base):
    """DTO for items."""

    id: int | None = None
    name: str
    description: str
    item_type: enums.ItemType
    stamina: int
    agility: int
    intelligence: int
    crit: int
    created_at: datetime | None = None
    updated_at: datetime | None = None


class NeoItemInputDTO(BaseModel):
    """DTO for items."""

    name: str
    description: str
    item_type: enums.ItemType
    stamina: int
    agility: int
    intelligence: int
    crit: int


class NeoItemUpdateDTO(BaseModel):
    """DTO for items."""

    name: str | None
    description: str
    item_type: enums.ItemType | None
    stamina: int | None
    agility: int | None
    intelligence: int | None
    crit: int | None


class NeoItemCharacterRelationshipInputDTO(BaseModel):
    """Input DTO for User relation with a character."""

    node2_id: int
    relationship_type: str
    relationship_props: dict[str, Any] = {}


class NeoItemCharacterRelationshipDTO(BaseRelationshipDTO):
    """User relation with a character, that validates the type of relationship given."""

    @validator("relationship_type")
    def validate_relationship_type(cls, v: Any) -> Any:
        allowed_types = ["HasItem"]
        if v not in allowed_types:
            raise ValueError(f"Invalid relationship type for item: {v}")
        return v


class NeoItemCharacterEquipRelationshipDTO(BaseRelationshipDTO):
    """User relation with a character, that validates the type of relationship given."""

    @validator("relationship_type")
    def validate_relationship_type(cls, v: Any) -> Any:
        allowed_types = [
            f"EquippedAs{item.name.capitalize()}" for item in enums.ItemType
        ]
        if v not in allowed_types:
            raise ValueError(f"Invalid relationship type for item equip: {v}")
        return v
