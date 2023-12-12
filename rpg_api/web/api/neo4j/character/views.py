from fastapi import APIRouter
from rpg_api.utils import dtos


router = APIRouter()


router.post("/")


async def create_character() -> dtos.EmptyDefaultResponse:
    return dtos.EmptyDefaultResponse()
