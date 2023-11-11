from rpg_api import exceptions as rpg_exc
from rpg_api.utils import dtos
from rpg_api.utils.dependencies import GetCurrentUser
from rpg_api.web.api.auth import auth_utils as utils
from fastapi.routing import APIRouter
from rpg_api.utils.daos import GetDAOs
from fastapi.responses import HTMLResponse
from fastapi import Request
from starlette.responses import Response
from rpg_api.services.templates import templates

router = APIRouter()


@router.post("/login-email")
async def login(
    input_dto: dtos.UserLoginDTO,
    daos: GetDAOs,
) -> dtos.DataResponse[dtos.LoginResponse]:
    """Login by email and password."""

    user = await daos.base_user.get_by_email(email=input_dto.email)

    if user is None:
        raise rpg_exc.HttpUnauthorized("Wrong email or password")

    is_valid_password = utils.verify_password(
        input_dto.password.get_secret_value(), user.password
    )

    if not is_valid_password:
        raise rpg_exc.HttpUnauthorized("Wrong email or password")

    token = utils.create_access_token(data=dtos.TokenData(user_id=str(user.id)))

    return dtos.DataResponse(data=dtos.LoginResponse(access_token=token))


@router.post("/register")
async def register(
    input_dto: dtos.UserCreateDTO,
    daos: GetDAOs,
) -> dtos.DefaultCreatedResponse:
    """Register by email and password."""

    user = await daos.base_user.get_by_email(email=input_dto.email)

    if user:
        raise rpg_exc.HttpForbidden("User already exists")

    await daos.base_user.create(
        dtos.BaseUserInputDTO(
            email=input_dto.email,
            password=utils.hash_password(input_dto.password.get_secret_value()),
            first_name=input_dto.first_name,
            last_name=input_dto.last_name,
            phone=input_dto.phone,
        )
    )

    return dtos.DefaultCreatedResponse()


@router.get("/me")
async def get_me(
    current_user: GetCurrentUser,
) -> dtos.DataResponse[dtos.BaseUserDTO]:
    """Get current user."""

    return dtos.DataResponse(data=current_user)


@router.get(
    "/login-html",
    response_class=HTMLResponse,
)
async def login_html(
    request: Request,
) -> Response:
    """Get current user."""

    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
        },
    )
