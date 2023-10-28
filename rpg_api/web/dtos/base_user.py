from pydantic import BaseModel, Field, EmailStr, SecretStr
from datetime import datetime


class BaseUserInsert(BaseModel):
    """Base DTO for mongoDB base_user insert."""

    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=1, max_length=50)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        """Config for BaseUserInsert."""

        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "example@hotmail.com",
                "password": "12345678",
                "created_at": "2021-08-30T15:19:05.000Z",
            }
        }
