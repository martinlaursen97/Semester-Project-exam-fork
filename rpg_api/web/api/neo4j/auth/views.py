from fastapi import APIRouter
from rpg_api.db.neo4j.dependencies import Neo4jSession
from rpg_api.web.dtos.neo4j.neo4j_dtos import (
    NeoBaseUserDTO,
    NeoUserCreateDTO,
)
from rpg_api.web.daos.base_user_dao import NeoBaseUserDAO
from rpg_api.utils import dtos
from rpg_api.web.api.postgres.auth import auth_utils as utils
from rpg_api import exceptions as rpg_exc
from rpg_api.services.email_service.email_dependencies import GetEmailService
from rpg_api.web.api.neo4j.auth.token_store import token_store
from rpg_api.settings import settings

router = APIRouter()


@router.post("/register")
async def register(
    session: Neo4jSession, input_dto: NeoUserCreateDTO
) -> dtos.DefaultCreatedResponse:
    """Register by email and password."""
    dao = NeoBaseUserDAO(session=session)
    user = await dao.get_by_email(email=input_dto.email)

    if user:
        raise rpg_exc.HttpForbidden("User already exists")

    await dao.create(
        input_dto=NeoBaseUserDTO(
            email=input_dto.email,
            password=utils.hash_password(input_dto.password.get_secret_value()),
        )
    )

    return dtos.DefaultCreatedResponse()


@router.post("/login-email")
async def login(
    input_dto: dtos.UserLoginDTO,
    session: Neo4jSession,
) -> dtos.DataResponse[dtos.LoginResponse]:
    """Login by email and password."""

    dao = NeoBaseUserDAO(session=session)
    user = await dao.get_by_email(email=input_dto.email)
    print(user)
    if user is None:
        raise rpg_exc.HttpUnauthorized("Wrong email or password")

    is_valid_password = utils.verify_password(
        input_dto.password.get_secret_value(), user.password
    )

    if not is_valid_password:
        raise rpg_exc.HttpUnauthorized("Wrong email or password")

    token = utils.create_access_token(data=dtos.TokenData(user_id=str(user.id)))

    return dtos.DataResponse(data=dtos.LoginResponse(access_token=token))


@router.post(
    "/forgot-password",
)
async def forgot_password(
    input_dto: dtos.ForgotPasswordDTO,
    email_service: GetEmailService,
    session: Neo4jSession,
) -> dtos.EmptyDefaultResponse:
    """Forgot password."""

    dao = NeoBaseUserDAO(session=session)
    user = await dao.get_by_email(email=input_dto.email)

    # We don't want to reveal if the user exists or not
    if user is None:
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

    print(token_store.tokens)
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
    session: Neo4jSession,
) -> dtos.EmptyDefaultResponse:
    """Reset password."""

    token_data = utils.decode_token(token=input_dto.token)
    dao = NeoBaseUserDAO(session=session)
    user = await dao.get_by_id(node_id=int(token_data.user_id))

    if user is None:
        raise rpg_exc.HttpUnauthorized("Token is invalid or user does not exist")
    print(token_store.tokens)
    stored_token = token_store.pop(user_id=int(token_data.user_id))
    if stored_token is None:
        raise rpg_exc.HttpUnauthorized(
            "Reset token has already been used, or has expired"
        )

    hashed_password = utils.hash_password(input_dto.new_password.get_secret_value())
    await dao.update(
        id=int(token_data.user_id),
        update_dto=dtos.NeoBaseUserUpdateDTO(
            password=hashed_password,
        ),
    )

    return dtos.EmptyDefaultResponse()
