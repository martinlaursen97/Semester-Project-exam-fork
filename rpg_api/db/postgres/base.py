from sqlalchemy.orm import DeclarativeBase

from rpg_api.db.postgres.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
