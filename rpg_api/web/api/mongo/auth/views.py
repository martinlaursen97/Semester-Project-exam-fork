from fastapi import APIRouter, Depends
from rpg_api.utils import dtos
from rpg_api.db.mongo.models.models import MBaseUser
from rpg_api import exceptions
from rpg_api.web.api.mongo.auth.auth_dependencies_mongo import get_current_user_mongo
from rpg_api.web.api.postgres.auth import auth_utils as utils

router = APIRouter()


@router.post("/login-email")
async def login(input_dto: dtos.UserLoginDTO) -> dtos.DataResponse[dtos.LoginResponse]:
    """Login by email and password."""

    user = await MBaseUser.get_by_email(input_dto.email)

    if user is None:
        raise exceptions.HttpUnauthorized("Wrong email or password")

    is_valid_password = utils.verify_password(
        input_dto.password.get_secret_value(), user.password
    )

    if not is_valid_password:
        raise exceptions.HttpUnauthorized("Wrong email or password")

    token = utils.create_access_token(data=dtos.TokenData(user_id=str(user.id)))

    return dtos.DataResponse(data=dtos.LoginResponse(access_token=token))


@router.post("/register")
async def register(user: MBaseUser) -> dtos.DefaultCreatedResponse:
    """Create a new user."""

    if await MBaseUser.get_by_email(user.email):
        raise exceptions.HttpBadRequest("User already exists.")

    user.password = utils.hash_password(user.password)
    await user.save()  # type: ignore

    return dtos.DefaultCreatedResponse()


@router.get("/me")
async def get_me(
    current_user: MBaseUser = Depends(get_current_user_mongo),
) -> dtos.DataResponse[MBaseUser]:
    """Get the current user."""

    return dtos.DataResponse(data=current_user)
