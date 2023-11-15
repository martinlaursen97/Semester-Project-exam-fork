from rpg_api.utils import dtos, models
from rpg_api.utils.dependencies import GetCurrentUser
from fastapi.routing import APIRouter
from rpg_api.utils.daos import GetDAOs
from sqlalchemy import orm
from rpg_api.utils.dependencies import GetCharacterIfUserOwns

router = APIRouter()


@router.get("")
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
            dtos.CharacterNestedWithClassAndLocationDTO.model_validate(c)
            for c in characters
        ]
    )


@router.post("")
async def create_character(
    endpoint_input_dto: dtos.CharacterPartialInputDTO,
    current_user: GetCurrentUser,
    daos: GetDAOs,
) -> dtos.DefaultCreatedResponse:
    """Create character."""

    input_dto = dtos.CharacterInputDTO(
        user_id=current_user.id,
        **endpoint_input_dto.model_dump(),
    )

    created_id = await daos.character.create(
        input_dto=input_dto,
    )

    return dtos.DefaultCreatedResponse(data=created_id)


@router.patch("/move/{character_id}")
async def move_character(
    update_dto: dtos.CharacterLocationUpdateDTO,
    character: GetCharacterIfUserOwns,
    daos: GetDAOs,
) -> dtos.EmptyDefaultResponse:
    """Move character."""

    await daos.character_location.update(
        id=character.character_location_id,  # type: ignore
        update_dto=update_dto,
    )

    return dtos.EmptyDefaultResponse()
