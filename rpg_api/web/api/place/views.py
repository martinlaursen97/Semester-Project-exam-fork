from loguru import logger
from rpg_api.utils import dtos
from fastapi.routing import APIRouter
from rpg_api.utils.daos import GetDAOs
from rpg_api import exceptions as rpg_exc


router = APIRouter()

import asyncio


@router.get("")  # , dependencies=[Depends(get_current_user)])
async def get_places(
    daos: GetDAOs,
) -> dtos.DataListResponse[dtos.PlaceDTO]:
    """Get all places."""

    places = await daos.place.filter()

    # loading example
    await asyncio.sleep(1)

    return dtos.DataListResponse(data=[dtos.PlaceDTO.model_validate(c) for c in places])


@router.post("")
async def create_place(
    input_dto: dtos.PlaceInputDTO,
    daos: GetDAOs,
) -> dtos.DefaultCreatedResponse:
    """Create place."""

    try:
        created_place_id = await daos.place.create(input_dto)
    except Exception as e:
        logger.exception(e)
        return dtos.DefaultCreatedResponse(
            message="Failed to create place.",
        )

    return dtos.DefaultCreatedResponse(
        data=created_place_id,
    )
