from rpg_api.utils import dtos
from fastapi import Depends
from fastapi.routing import APIRouter
from rpg_api.utils.daos import GetDAOs
from pydantic import BaseModel, Field


from rpg_api import exceptions


router = APIRouter()


class PlaceFilterDTO(BaseModel):
    """Search DTO for Place."""

    search: str | None = Field(
        None,
        description="Search for places by name/description.",
    )


@router.get("", status_code=200)
async def get_places(
    daos: GetDAOs,
    filter_dto: PlaceFilterDTO = Depends(),
) -> dtos.DataListResponse[dtos.PlaceDTO]:
    """Get all places."""

    return dtos.DataListResponse(
        data=await daos.place.by_search(filter_dto.search)
        if filter_dto.search
        else [dtos.PlaceDTO.model_validate(c) for c in await daos.place.filter()]
    )


@router.post("", status_code=201)
async def create_place(
    input_dto: dtos.PlaceInputDTO,
    daos: GetDAOs,
) -> dtos.DefaultCreatedResponse:
    """Create place."""

    place_name_taken = await daos.place.filter_first(name=input_dto.name)

    if place_name_taken:
        raise exceptions.HttpBadRequest("Place name already taken")

    place_overlaps = await daos.place.check_overlaps(
        input_dto.x, input_dto.y, input_dto.radius
    )

    if place_overlaps:
        raise exceptions.HttpBadRequest("New place overlaps with existing place")

    return dtos.DefaultCreatedResponse(data=await daos.place.create(input_dto))
