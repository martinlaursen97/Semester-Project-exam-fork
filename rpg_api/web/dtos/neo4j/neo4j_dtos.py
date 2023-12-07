from pydantic import BaseModel, validator, EmailStr, SecretStr, Field
from rpg_api.db.neo4j.base import Base, BaseRelationshipDTO
from typing import Any
from rpg_api import constants


class NeoBaseUserModel(Base):
    """Model for creating a person. Label must be given when creating a model."""

    __label__ = "BaseUser"
    id: int | None = None
    email: str
    password: str


class NeoBaseUserDTO(BaseModel):
    """DTO for person."""

    email: str
    password: str


class NeoBaseUserResponseDTO(BaseModel):
    """DTO for person."""

    id: int
    email: str
    password: str


class NeoUserCreateDTO(BaseModel):
    """DTO for creating a user."""

    email: EmailStr
    password: SecretStr = Field(
        ...,
        min_length=constants.MIN_LENGTH_PASSWORD,
        max_length=constants.MAX_LENGTH_PASSWORD,
    )


class NeoBaseUserUpdateDTO(BaseModel):
    """Update DTO for person."""

    email: str | None = None
    password: str | None = None


class NeoBaseUserRelationshipDTO(BaseRelationshipDTO):
    """Base user relation model, that validates the type of relationship given."""

    @validator("relationship_type")
    def validate_relationship_type(cls, v: Any) -> Any:
        allowed_types = ["friend", "blocked"]
        if v not in allowed_types:
            raise ValueError(f"Invalid relationship type for User: {v}")
        return v
