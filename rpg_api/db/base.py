from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import uuid

from rpg_api.db.meta import meta
import sqlalchemy as sa
from rpg_api import utils
from datetime import datetime


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta

    id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), default=utils.get_datetime_utc()
    )
