from rpg_api.utils import dtos, models
from rpg_api.utils.dependencies import GetCurrentUser
from fastapi.routing import APIRouter
from rpg_api.utils.daos import GetDAOs
from sqlalchemy import orm
from rpg_api.utils.dependencies import GetCharacterIfUserOwns
from pydantic import BaseModel
from rpg_api import exceptions

router = APIRouter()


class CharacterPlaceDTO(BaseModel):
    """Character place DTO."""

    name: str


@router.get("", status_code=200)
async def characters_me(
    daos: GetDAOs,
    current_user: GetCurrentUser,
) -> dtos.DataListResponse[dtos.CharacterNestedWithClassAndLocationDTO]:
    """My characters."""

    characters = await daos.character.filter(
        user_id=current_user.id,
        loads=[
            orm.joinedload(models.Character.base_class),
            orm.joinedload(models.Character.character_location),
        ],
    )

    return dtos.DataListResponse(
        data=[
            dtos.CharacterNestedWithClassAndLocationDTO.model_validate(character)
            for character in characters
        ]
    )


@router.get("/place/{character_id}", status_code=200)
async def character_place_details(
    daos: GetDAOs,
    character: GetCharacterIfUserOwns,
) -> dtos.DataResponse[CharacterPlaceDTO]:
    """Get place of character."""

    place_name = await daos.character.get_place(
        character_id=character.id,
    )
    return dtos.DataResponse(data=CharacterPlaceDTO(name=place_name))


@router.post("", status_code=201)
async def create_character(
    endpoint_input_dto: dtos.CharacterPartialInputDTO,
    current_user: GetCurrentUser,
    daos: GetDAOs,
) -> dtos.DefaultCreatedResponse:
    """Create character."""

    character_name_taken = (
        await daos.character.filter_first(
            character_name=endpoint_input_dto.character_name,
        )
        is not None
    )

    if character_name_taken:
        raise exceptions.HttpForbidden("Character name already taken")

    input_dto = dtos.CharacterInputDTO(
        user_id=current_user.id,
        **endpoint_input_dto.model_dump(),
    )

    created_id = await daos.character.create(
        input_dto=input_dto,
    )

    return dtos.DefaultCreatedResponse(data=created_id)
