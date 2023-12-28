from rpg_api.utils import dtos
from rpg_api.utils.dependencies import GetCurrentUser
from fastapi.routing import APIRouter
from rpg_api.utils.daos import GetDAOs

router = APIRouter()


@router.delete("", status_code=200)
async def delete_current_user(
    current_user: GetCurrentUser,
    daos: GetDAOs,
) -> dtos.EmptyDefaultResponse:
    """Delete current user."""

    await daos.base_user.delete(
        id=current_user.id,
    )

    return dtos.EmptyDefaultResponse()
