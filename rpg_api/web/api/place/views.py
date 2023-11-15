from rpg_api.utils import dtos
from fastapi.routing import APIRouter
from rpg_api.utils.daos import GetDAOs


router = APIRouter()


@router.get("")  # , dependencies=[Depends(get_current_user)])
async def get_places(
    daos: GetDAOs,
) -> dtos.DataListResponse[dtos.PlaceDTO]:
    """Get all places."""

    places = await daos.place.filter()

    return dtos.DataListResponse(data=[dtos.PlaceDTO.model_validate(c) for c in places])
