from beanie import PydanticObjectId
from fastapi import APIRouter, Depends
from rpg_api.utils import dtos
from rpg_api.db.mongo.models.models import MBaseUser
from rpg_api import exceptions
from rpg_api.web.api.mongo.auth.auth_dependencies_mongo import get_current_user_mongo

router = APIRouter()


@router.post("/add-friend")
async def add_friend(
    friend_id: PydanticObjectId,
    current_user: MBaseUser = Depends(get_current_user_mongo),
) -> dtos.DefaultCreatedResponse:
    """Add a friend to the current user."""

    if current_user.id == friend_id:
        raise exceptions.HttpBadRequest("You can't add yourself as a friend.")

    await current_user.update({"$push": {"friends": friend_id}})
    return dtos.DefaultCreatedResponse()


@router.delete("/remove-friend")
async def remove_friend(
    friend_id: PydanticObjectId,
    current_user: MBaseUser = Depends(get_current_user_mongo),
) -> dtos.EmptyDefaultResponse:
    """Remove a friend from the current user."""

    await current_user.update({"$pull": {"friends": friend_id}})
    return dtos.EmptyDefaultResponse()
