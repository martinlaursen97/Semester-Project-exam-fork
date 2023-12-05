from fastapi import APIRouter

from rpg_api.web.api.mongo.views import router

mongo_router = APIRouter()


mongo_router.include_router(router, prefix="/temp")
