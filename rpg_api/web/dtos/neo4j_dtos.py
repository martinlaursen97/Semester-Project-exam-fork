from pydantic import BaseModel, validator
from rpg_api.db.neo4j.base import Base, BaseRelationshipDTO
from typing import Any


class PersonModel(Base):
    """Model for creating a person. Label must be given when creating a model."""

    __label__ = "Person"
    name: str
    age: int


class PersonDTO(BaseModel):
    """DTO for person."""

    name: str
    age: int


class PersonUpdateDTO(BaseModel):
    """Update DTO for person."""

    name: str


class PersonRelationshipDTO(BaseRelationshipDTO):
    """Person relation model, that validates the type of relationship given."""

    @validator("relationship_type")
    def validate_relationship_type(cls, v: Any) -> Any:
        allowed_types = ["friend", "blocked"]
        if v not in allowed_types:
            raise ValueError(f"Invalid relationship type for Person: {v}")
        return v
