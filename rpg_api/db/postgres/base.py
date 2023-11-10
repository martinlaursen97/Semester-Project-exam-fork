from rpg_api.db.postgres.meta import meta
import uuid

import sqlalchemy as sa
from rpg_api.utils import date_utils
from datetime import datetime
from typing import Any
from collections.abc import Callable

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base setup for all models including UUID."""

    metadata = meta

    __tablename__: str
    __init__: Callable[..., Any]
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), default=date_utils.get_datetime_utc()
    )
