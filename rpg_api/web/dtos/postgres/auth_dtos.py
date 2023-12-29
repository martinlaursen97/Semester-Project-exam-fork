from pydantic import BaseModel, EmailStr, SecretStr, Field

from rpg_api import constants


class TokenData(BaseModel):
    """Token data."""

    user_id: str


class LoginResponse(BaseModel):
    """Response DTO for access token."""

    access_token: str


class UserLoginDTO(BaseModel):
    """DTO for logging in with user."""

    email: EmailStr = Field(
        ...,
        min_length=constants.MIN_LENGTH_EMAIL,
        max_length=constants.MAX_LENGTH_EMAIL,
    )
    password: SecretStr = Field(
        ...,
        min_length=constants.MIN_LENGTH_PASSWORD,
        max_length=constants.MAX_LENGTH_PASSWORD,
    )


class UserCreateDTO(BaseModel):
    """DTO for creating a user."""

    email: EmailStr
    password: SecretStr = Field(
        ...,
        min_length=constants.MIN_LENGTH_PASSWORD,
        max_length=constants.MAX_LENGTH_PASSWORD,
    )


class ResetPasswordDTO(BaseModel):
    """DTO for resetting password."""

    token: str
    new_password: SecretStr = Field(
        ...,
        min_length=constants.MIN_LENGTH_PASSWORD,
        max_length=constants.MAX_LENGTH_PASSWORD,
    )


class ForgotPasswordDTO(BaseModel):
    """DTO for requesting a password reset."""

    email: EmailStr
