from fastapi import Depends
from pydantic import BaseModel, Field

from rpg_api import exceptions as exc
from rpg_api.utils import dtos
from rpg_api.utils.daos import AllDAOs
from rpg_api.web.api.auth import auth_utils
from rpg_api.web.api.auth.auth_dependencies import get_current_user
from rpg_api.web.api.router import APIRouter

router = APIRouter()


@router.get("/me")
async def get_user_me(
    current_user: dtos.UserDTO = Depends(get_current_user),
) -> dtos.DataResponse[dtos.UserDTO]:
    """Get current user"""
    return dtos.DataResponse(data=current_user)
