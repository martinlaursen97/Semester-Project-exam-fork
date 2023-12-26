from pydantic import BaseModel
from typing import Any


class Base(BaseModel):
    """Base setup for all models."""

    __label__: str


class BaseRelationshipDTO(BaseModel):
    """Base relationship DTO, for creating a relationship."""

    node1_id: int
    node2_id: int
    relationship_type: str
    relationship_props: dict[str, Any] = {}
