from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class BaseUserInsert(BaseModel):
    """Base DTO for mongoDB base_user insert."""

    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=1, max_length=50)
    created_at: datetime = Field(default_factory=datetime.utcnow)
