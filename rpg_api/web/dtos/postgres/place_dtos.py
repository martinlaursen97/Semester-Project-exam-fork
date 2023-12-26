from pydantic import BaseModel
from uuid import UUID
from rpg_api.utils import dtos


class PlaceBaseDTO(dtos.OrmBasicModel):
    """Base DTO for Place."""

    name: str
    description: str | None = None
    radius: float
    x: int
    y: int


class PlaceDTO(PlaceBaseDTO):
    """DTO for Place."""

    id: UUID


class PlaceInputDTO(PlaceBaseDTO):
    """Input DTO for Place."""


class PlaceUpdateDTO(BaseModel):
    """Update DTO for Place."""

    name: str | None = None
    description: str | None = None
    radius: float | None = None
    x: int | None = None
    y: int | None = None
