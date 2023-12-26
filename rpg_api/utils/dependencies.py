from rpg_api.web.api.postgres.auth.auth_dependencies import (
    get_current_user,
    get_token,
    GetCurrentUser,
    get_character_if_user_owns,
    GetCharacterIfUserOwns,
)
from rpg_api.web.api.mongo.auth.auth_dependencies_mongo import get_current_user_mongo
