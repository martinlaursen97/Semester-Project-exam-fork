from pydantic import BaseModel, Field
from uuid import UUID
from rpg_api.utils import dtos
from rpg_api import constants


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

    name: str = Field(
        ...,
        min_length=constants.MIN_LENGTH_PLACE_NAME,
        max_length=constants.MAX_LENGTH_PLACE_NAME,
    )
    description: str | None = None
    radius: float = Field(
        default=0,
        ge=0,
    )
    x: int = 0
    y: int = 0


class PlaceUpdateDTO(BaseModel):
    """Update DTO for Place."""

    name: str | None = Field(
        None,
        min_length=constants.MIN_LENGTH_PLACE_NAME,
        max_length=constants.MAX_LENGTH_PLACE_NAME,
    )
    description: str | None = Field(
        None,
        max_length=constants.MAX_LENGTH_DESCRIPTION,
    )
    radius: float | None = None
    x: int | None = None
    y: int | None = None
