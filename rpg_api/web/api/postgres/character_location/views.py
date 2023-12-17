from rpg_api.utils import dtos
from fastapi.routing import APIRouter
from rpg_api.utils.daos import GetDAOs
from rpg_api.utils.dependencies import GetCharacterIfUserOwns

router = APIRouter()


@router.patch("/{character_id}", status_code=200)
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
