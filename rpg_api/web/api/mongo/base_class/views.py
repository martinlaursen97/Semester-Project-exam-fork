from beanie import PydanticObjectId
from fastapi import APIRouter
from rpg_api.utils import dtos
from rpg_api.db.mongo.models.models import (
    MClass,
    MAbility,
)
from pydantic import BaseModel
from rpg_api import exceptions

router = APIRouter()


class AbilityDTO(BaseModel):
    """DTO for creating an ability."""

    name: str
    description: str


class ClassCreateRequest(BaseModel):
    """DTO for creating a class."""

    name: str
    description: str
    abilities: list[AbilityDTO]


@router.post("")
async def create_class(
    input_dto: ClassCreateRequest,
) -> dtos.DefaultCreatedResponse:
    """Create a class for the current user."""

    if await MClass.find_one({"name": input_dto.name}):
        raise exceptions.HttpBadRequest("Class with this name already exists.")

    ability_name_exists = await MAbility.find_one(
        {"name": {"$in": [ability.name for ability in input_dto.abilities]}}
    )

    if ability_name_exists:
        raise exceptions.HttpBadRequest("Non-unique ability name found.")

    class_ = MClass(
        name=input_dto.name,
        description=input_dto.description,
        abilities=[
            await MAbility(**ability.model_dump()).save()  # type: ignore
            for ability in input_dto.abilities
        ],
    )
    await class_.save()  # type: ignore

    return dtos.DefaultCreatedResponse()


@router.patch("/{class_id}/add-ability")
async def add_ability(
    class_id: PydanticObjectId,
    ability_id: PydanticObjectId,
) -> dtos.DefaultCreatedResponse:
    """Add an ability to a class."""

    class_ = await MClass.get(class_id)

    if class_ is None:
        raise exceptions.HttpNotFound("Class not found.")

    ability = await MAbility.get(ability_id)

    if ability is None:
        raise exceptions.HttpNotFound("Ability not found.")

    await class_.update({"$push": {"abilities": ability_id}})

    return dtos.DefaultCreatedResponse()
