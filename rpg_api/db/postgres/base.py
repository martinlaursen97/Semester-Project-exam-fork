from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import TSVECTOR
import uuid

import sqlalchemy as sa
from rpg_api.utils import date_utils
from datetime import datetime
from rpg_api.db.postgres.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta

    id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), default=date_utils.get_datetime_utc()
    )


class TSVector(sa.types.TypeDecorator):  # type: ignore
    """TSVector type for postgresql."""

    impl = TSVECTOR
    cache_ok = True


class AbstractSearchableModel(Base):
    """Abstract search name/description mixin model."""

    __abstract__ = True

    name: Mapped[str] = mapped_column(sa.String(50), unique=True)
    description: Mapped[str | None] = mapped_column(sa.String(500))

    ts_vector = sa.Column(  # type: ignore
        TSVector(),
        sa.Computed(
            "to_tsvector('english', name || ' ' || description)",
            persisted=True,
        ),
    )
