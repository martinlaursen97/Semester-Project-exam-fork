from pydantic import BaseModel, validator, EmailStr, SecretStr, Field
from rpg_api.db.neo4j.base import Base, BaseRelationshipDTO
from typing import Any
from rpg_api import constants
from datetime import datetime


class NeoBaseUserModel(Base):
    """Model for creating a person. Label must be given when creating a model."""

    __label__ = "BaseUser"
    id: int | None = None
    email: str
    password: str


class NeoBaseUserDTO(BaseModel):
    """DTO for BaseUser."""

    email: str
    password: str


class NeoBaseUserResponseLoginDTO(NeoBaseUserDTO):
    """DTO for Login response."""

    id: int


class NeoBaseUserResponseDTO(NeoBaseUserResponseLoginDTO):
    """DTO for BaseUserResponse."""

    email: str


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


class NeoBaseUserRelationshipInputDTO(BaseModel):
    """DTO for creating a relationship between two users."""

    friend_id: int
    relationship_type: str
    relationship_props: dict[str, Any] = {"created_at": datetime.now()}


class NeoBaseUserRelationshipDTO(BaseRelationshipDTO):
    """Base user relation model, that validates the type of relationship given."""

    @validator("relationship_type")
    def validate_relationship_type(cls, v: Any) -> Any:
        allowed_types = ["Friends", "Blocked"]
        if v not in allowed_types:
            raise ValueError(f"Invalid relationship type for User: {v}")
        return v
