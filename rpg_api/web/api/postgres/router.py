from fastapi.routing import APIRouter

from rpg_api.web.api.postgres import auth
from rpg_api.web.api.postgres import character
from rpg_api.web.api.postgres import base_class
from rpg_api.web.api.postgres import place
from rpg_api.web.api.postgres import character_location


pg_router = APIRouter(tags=["postgres"])

pg_router.include_router(auth.router, prefix="/auth")
pg_router.include_router(character.router, prefix="/characters")
pg_router.include_router(character_location.router, prefix="/character-locations")
pg_router.include_router(base_class.router, prefix="/base-classes")
pg_router.include_router(place.router, prefix="/places")
