from datetime import datetime
from uuid import UUID


from pydantic import BaseModel, EmailStr
from rpg_api.core.dtos.base_schemas import OrmBasicModel

from rpg_api.enums import UserStatus


class BaseUserInputDTO(BaseModel):
    """DTO for creating a user."""

    email: str
    password: str
    status: UserStatus = UserStatus.active
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None


class BaseUserUpdateDTO(BaseModel):
    """DTO for updating a user."""

    email: EmailStr | None = None
    password: str | None = None


class BaseUserDTO(OrmBasicModel):
    """DTO for returning a user."""

    id: UUID
    email: EmailStr
    status: UserStatus
    first_name: str | None
    last_name: str | None
    phone: str | None
    created_at: datetime
