from pydantic import BaseModel
from uuid import UUID
from rpg_api.core.dtos.base_schemas import OrmBasicModel


class CharacterLocationDTO(OrmBasicModel):
    """DTO for CharacterLocation."""

    id: UUID
    base_character_id: UUID
    x: int
    y: int


class CharacterLocationInputDTO(BaseModel):
    """Input DTO for CharacterLocation."""

    base_character_id: UUID
    x: int
    y: int


class CharacterLocationUpdateDTO(BaseModel):
    """Update DTO for CharacterLocation."""

    base_character_id: UUID | None = None
    x: int | None = None
    y: int | None = None
