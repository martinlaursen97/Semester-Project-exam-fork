from beanie import PydanticObjectId, WriteRules
from fastapi import APIRouter, Depends
from rpg_api.enums import Gender
from rpg_api.utils import dtos
from rpg_api.db.mongo.models.models import (
    EmbedAttribute,
    MBaseUser,
    MCharacter,
    MClass,
    MAttributeType,
    EmbedCharacterDetails,
    EmbedLocation,
)
from rpg_api.web.api.mongo.auth.auth_dependencies_mongo import get_current_user_mongo
from pydantic import BaseModel
from rpg_api import exceptions

router = APIRouter()


class CharacterDetailsCreate(BaseModel):
    """DTO for creating character details."""

    character_name: str
    gender: Gender


class CharacterCreateRequest(BaseModel):
    """DTO for creating a character."""

    class_id: PydanticObjectId
    details: CharacterDetailsCreate


# TODO: Each class should have a unique set of initial attributes
INITIAL_ATTRIBUTES = [
    EmbedAttribute(attribute=MAttributeType.strength),
    EmbedAttribute(attribute=MAttributeType.dexterity),
    EmbedAttribute(attribute=MAttributeType.intelligence),
]


@router.post("")
async def create_character(
    input_dto: CharacterCreateRequest,
    user: MBaseUser = Depends(get_current_user_mongo),
) -> dtos.DefaultCreatedResponse:
    """Create a character for the current user."""

    class_ = await MClass.get(input_dto.class_id)

    if class_ is None:
        raise exceptions.HttpNotFound("Class not found.")

    if await MCharacter.find_one({"character_name": input_dto.details.character_name}):
        raise exceptions.HttpBadRequest("Character with this name already exists.")

    character = MCharacter(
        user=user,  # type: ignore
        class_=class_,  # type: ignore
        character_attributes=INITIAL_ATTRIBUTES,
        location=EmbedLocation(x=0, y=0),
        details=EmbedCharacterDetails(**input_dto.details.model_dump()),
    )

    await character.insert(link_rule=WriteRules.WRITE)  # type: ignore
    await user.update({"$push": {"characters": character.id}})

    return dtos.DefaultCreatedResponse()
