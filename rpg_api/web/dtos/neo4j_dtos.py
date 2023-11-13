from pydantic import BaseModel
from rpg_api.db.neo4j.base import Base


class PersonModel(Base):
    __label__ = "Person"
    name: str
    age: int


class PersonInputDTO(BaseModel):
    name: str
    age: int


class PersonUpdateDTO(BaseModel):
    name: str
