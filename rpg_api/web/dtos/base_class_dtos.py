from pydantic import BaseModel
from uuid import UUID
from rpg_api.core.dtos.base_schemas import OrmBasicModel


class BaseClassDTO(OrmBasicModel):
    """Base class DTO."""

    id: UUID
    name: str


class BaseClassSimpleDTO(OrmBasicModel):
    """Base class simple DTO."""

    name: str


class BaseClassInputDTO(BaseModel):
    """Base class input DTO."""

    name: str


class BaseClassUpdateDTO(BaseModel):
    """Base class update DTO."""

    name: str | None = None
