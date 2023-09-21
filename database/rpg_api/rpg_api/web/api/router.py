from fastapi.routing import APIRouter
from fastapi import Depends
from rpg_api.db.dependencies import get_db_session
from sqlalchemy import text

from rpg_api.web.api import monitoring

api_router = APIRouter()
api_router.include_router(monitoring.router)


@api_router.get("/")
def hello_world() -> None:
    return "Hello world"


@api_router.get("/base-char")
def get_base_chars_from_view(dbsession=Depends(get_db_session)):
    result = dbsession.execute(text("SELECT * FROM base_char_view")).fetchall()
    columns = result[0].keys()
    return [dict(zip(columns, row)) for row in result]
