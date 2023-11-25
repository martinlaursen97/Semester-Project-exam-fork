from rpg_api.utils import dtos
from fastapi.routing import APIRouter
from rpg_api.utils.daos import GetDAOs


router = APIRouter()


@router.get("")  # , dependencies=[Depends(get_current_user)])
async def get_classes(
    daos: GetDAOs,
) -> dtos.DataListResponse[dtos.BaseClassDTO]:
    """Get all classes."""

    classes = await daos.base_class.filter()

    return dtos.DataListResponse(
        data=[dtos.BaseClassDTO.model_validate(c) for c in classes]
    )
