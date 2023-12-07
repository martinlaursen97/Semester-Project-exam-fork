from fastapi import APIRouter

from rpg_api.web.api.mongo.auth import router as auth_router
from rpg_api.web.api.mongo.base_user import router as base_user_router

mongo_router = APIRouter()


mongo_router.include_router(auth_router, prefix="/auth")
mongo_router.include_router(base_user_router, prefix="/base-user")
