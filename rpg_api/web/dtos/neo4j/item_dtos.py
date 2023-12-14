from rpg_api.db.neo4j.base import Base, BaseRelationshipDTO
from rpg_api import enums
from datetime import datetime
from pydantic import BaseModel


class NeoItemModel(Base):
    """Model for items."""

    __label__ = "Item"

    id: int | None = None
    name: str
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
    item_type: enums.ItemType
    stamina: int
    agility: int
    intelligence: int
    crit: int


class NeoItemUpdateDTO(BaseModel):
    """DTO for items."""

    name: str | None
    item_type: enums.ItemType | None
    stamina: int | None
    agility: int | None
    intelligence: int | None
    crit: int | None