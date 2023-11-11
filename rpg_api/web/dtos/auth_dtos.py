from pydantic import BaseModel, EmailStr, SecretStr, Field


class TokenData(BaseModel):
    """Token data."""

    user_id: str


class LoginResponse(BaseModel):
    """Response DTO for access token."""

    access_token: str


class UserLoginDTO(BaseModel):
    """DTO for logging in with user."""

    email: EmailStr
    password: SecretStr


class UserCreateDTO(BaseModel):
    """DTO for creating a user."""

    email: EmailStr
    password: SecretStr = Field(..., min_length=8, max_length=32)
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
