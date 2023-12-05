from beanie import Document, Indexed

from pydantic import Field
import datetime
from typing import Annotated

from rpg_api.utils.date_utils import get_datetime_utc


class MBase(Document):
    """Base model for mongodb."""

    created_at: datetime.datetime = Field(default_factory=get_datetime_utc)


class MNameDescriptionMixin(Document):
    """Mixin for name and description fields."""

    name: Annotated[str, Indexed(unique=True), Field(max_length=50)]
    description: Annotated[str, Field(max_length=500)]
