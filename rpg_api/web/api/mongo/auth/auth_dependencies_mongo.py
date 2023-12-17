from beanie import PydanticObjectId
from rpg_api.db.mongo.models.models import MBaseUser
from fastapi import Depends

from rpg_api.web.api.postgres.auth import auth_utils
from rpg_api.web.api.postgres.auth.auth_dependencies import get_token
from rpg_api import exceptions


async def get_current_user_mongo(token: str = Depends(get_token)) -> MBaseUser:
    """Get current user from token data."""
    token_data = auth_utils.decode_token(token)

    user = await MBaseUser.get(PydanticObjectId(token_data.user_id))

    if user is None:
        raise exceptions.HttpNotFound("Decoded user not found.")

    return user
