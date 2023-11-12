from rpg_api.utils import dtos, models
from rpg_api.utils.dependencies import GetCurrentUser
from fastapi.routing import APIRouter
from rpg_api.utils.daos import GetDAOs
from sqlalchemy import orm


router = APIRouter()


@router.get("")
async def characters_me(
    daos: GetDAOs,
    current_user: GetCurrentUser,
) -> dtos.DataListResponse[dtos.BaseCharacterNestedWithClassDTO]:
    """My characters."""

    characters = await daos.base_character.filter(
        user_id=current_user.id,
        loads=[
            orm.joinedload(models.BaseCharacter.base_class),
        ],
    )

    return dtos.DataListResponse(
        data=[
            dtos.BaseCharacterNestedWithClassDTO.model_validate(c) for c in characters
        ]
    )


@router.post("")
async def create_character(
    endpoint_input_dto: dtos.BaseCharacterPartialInputDTO,
    current_user: GetCurrentUser,
    daos: GetDAOs,
) -> dtos.DefaultCreatedResponse:
    """Create character."""

    input_dto = dtos.BaseCharacterInputDTO(
        user_id=current_user.id,
        **endpoint_input_dto.model_dump(),
    )

    created_id = await daos.base_character.create(
        input_dto=input_dto,
    )

    return dtos.DefaultCreatedResponse(data=created_id)
