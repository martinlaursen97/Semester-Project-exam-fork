from pydantic import BaseModel


class Base(BaseModel):
    """Base setup for all models."""

    __label__: str
