from loguru import logger
from rpg_api import exceptions
from rpg_api.services.email_service.email_dependencies import GetEmailService
from rpg_api.utils import dtos
from rpg_api.web.api.auth import auth_utils as utils
from rpg_api.web.api.auth.token_store import token_store
from fastapi.routing import APIRouter
from rpg_api.utils.daos import GetDAOs
from rpg_api.settings import settings

router = APIRouter()


@router.post("/login-email")
async def login(
    input_dto: dtos.UserLoginDTO,
    daos: GetDAOs,
) -> dtos.DataResponse[dtos.LoginResponse]:
    """Login by email and password."""

    user = await daos.base_user.filter_first(email=input_dto.email)

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
async def register(
    input_dto: dtos.UserCreateDTO,
    daos: GetDAOs,
) -> dtos.DefaultCreatedResponse:
    """Register by email and password."""

    user = await daos.base_user.filter(email=input_dto.email)

    if user:
        raise exceptions.HttpForbidden("User already exists")

    await daos.base_user.create(
        dtos.BaseUserInputDTO(
            email=input_dto.email,
            password=utils.hash_password(input_dto.password.get_secret_value()),
        )
    )

    return dtos.DefaultCreatedResponse()


@router.post(
    "/forgot-password",
)
async def forgot_password(
    input_dto: dtos.ForgotPasswordDTO,
    email_service: GetEmailService,
    daos: GetDAOs,
) -> dtos.EmptyDefaultResponse:
    """Forgot password."""

    user = await daos.base_user.filter_first(email=input_dto.email)

    # We don't want to reveal if the user exists or not
    if user is None:
        logger.info(f"User {input_dto.email} does not exist")
        return dtos.EmptyDefaultResponse()

    # Create and store token which will be used to reset the password
    token = utils.create_reset_password_token(
        data=dtos.TokenData(
            user_id=str(user.id),
        )
    )
    token_store.set(
        user_id=user.id,
        token=token,
    )

    html = f"""
    <html>
        <head></head>
        <body>
            <p>Click the link below to reset your password:</p>
            <a href="{settings.frontend_url}/reset-password?token={token}">
                Reset password
            </a>
        </body>
    </html>
    """

    email = dtos.EmailDTO(
        email=input_dto.email,
        subject="Forgot password",
        body=f"Hello {user.email}!",
        html=html,
    )
    await email_service.send_email(email)

    return dtos.EmptyDefaultResponse()


@router.post("/reset-password")
async def reset_password(
    input_dto: dtos.ResetPasswordDTO,
    daos: GetDAOs,
) -> dtos.EmptyDefaultResponse:
    """Reset password."""

    token_data = utils.decode_token(token=input_dto.token)
    user = await daos.base_user.filter_first(id=token_data.user_id)

    if user is None:
        raise exceptions.HttpUnauthorized("Token is invalid or user does not exist")

    stored_token = token_store.pop(user_id=user.id)
    if stored_token is None:
        raise exceptions.HttpUnauthorized(
            "Reset token has already been used, or has expired"
        )

    hashed_password = utils.hash_password(input_dto.new_password.get_secret_value())
    await daos.base_user.update(
        id=user.id,
        update_dto=dtos.BaseUserUpdateDTO(
            password=hashed_password,
        ),
    )

    logger.info(f"Password reset for user {user.email}")
    return dtos.EmptyDefaultResponse()
