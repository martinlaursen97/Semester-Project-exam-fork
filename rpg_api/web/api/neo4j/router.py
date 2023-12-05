from fastapi import APIRouter

from rpg_api.web.api.neo4j import users

neo4j_router = APIRouter()


neo4j_router.include_router(users.router, prefix="/users")
