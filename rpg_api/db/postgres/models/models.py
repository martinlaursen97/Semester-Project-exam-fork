from rpg_api.db.postgres.base import Base
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from rpg_api.enums import UserStatus, Gender
import uuid
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class BaseUser(Base):
    """User model."""

    __tablename__ = "base_user"

    email: Mapped[str] = mapped_column(sa.String(100), unique=True)
    password: Mapped[str] = mapped_column(sa.String(255))
    status: Mapped[UserStatus] = mapped_column(
        sa.Enum(UserStatus, name="user_status"), default=UserStatus.active
    )

    __table_args__ = (
        sa.Index("idx_base_user_email", email),
        sa.Index("idx_base_user_status", status),
    )


class AbilityType(Base):
    """Ability type model."""

    __tablename__ = "ability_type"

    name: Mapped[str] = mapped_column(sa.String(50), unique=True)
    description: Mapped[str] = mapped_column(sa.String(500))

    __table_args__ = (sa.Index("idx_ability_type_name", name),)


class BaseClass(Base):
    """Model for base class."""

    __tablename__ = "base_class"

    name: Mapped[str] = mapped_column(sa.String(50), unique=True)

    __table_args__ = (sa.Index("idx_base_class_name", name),)


class Attribute(Base):
    """Model for Attribute."""

    __tablename__ = "attribute"

    name: Mapped[str] = mapped_column(
        sa.String(50),
        unique=True,
    )
    description: Mapped[str] = mapped_column(sa.String(500))

    __table_args__ = (sa.Index("idx_attribute_name", name),)


class Place(Base):
    """Model for place."""

    __tablename__ = "place"

    name: Mapped[str] = mapped_column(sa.String(50), unique=True)
    radius: Mapped[int] = mapped_column(sa.Integer)
    x: Mapped[int] = mapped_column(sa.Integer)
    y: Mapped[int] = mapped_column(sa.Integer)

    __table_args__ = (sa.Index("idx_place_name", name),)


class Relation(Base):
    """Model for relations."""

    __tablename__ = "relation"

    user1_id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(as_uuid=True), ForeignKey("base_user.id", ondelete="CASCADE")
    )
    user2_id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(as_uuid=True), ForeignKey("base_user.id", ondelete="CASCADE")
    )

    user1: Mapped["BaseUser"] = relationship(
        "BaseUser", foreign_keys=[user1_id], uselist=False
    )
    user2: Mapped["BaseUser"] = relationship(
        "BaseUser", foreign_keys=[user2_id], uselist=False
    )

    __table_args__ = (
        sa.UniqueConstraint("user1_id", "user2_id", name="uq_relation_user1_user2"),
    )


class Character(Base):
    """Model for character."""

    __tablename__ = "character"

    base_class_id: Mapped[uuid.UUID | None] = mapped_column(
        sa.UUID(as_uuid=True),
        ForeignKey("base_class.id", ondelete="SET NULL"),
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(as_uuid=True),
        ForeignKey("base_user.id", ondelete="CASCADE"),
    )
    character_location_id: Mapped[uuid.UUID | None] = mapped_column(
        sa.UUID(as_uuid=True),
        ForeignKey("character_location.id", ondelete="SET NULL"),
    )
    gender: Mapped[Gender] = mapped_column(
        sa.Enum(Gender, name="gender"), default=Gender.other
    )
    character_name: Mapped[str] = mapped_column(sa.String(50), unique=True)
    alive: Mapped[bool] = mapped_column(sa.Boolean, default=True)
    level: Mapped[int] = mapped_column(sa.Integer, default=1)
    xp: Mapped[int] = mapped_column(sa.Integer, default=1)
    money: Mapped[int] = mapped_column(sa.Integer, default=1)

    base_class: Mapped["BaseClass | None"] = relationship(
        "BaseClass", foreign_keys=[base_class_id]
    )
    user: Mapped["BaseUser"] = relationship("BaseUser", foreign_keys=[user_id])
    character_location: Mapped["CharacterLocation | None"] = relationship(
        "CharacterLocation",
        foreign_keys=[character_location_id],
        uselist=False,
    )

    __table_args__ = (
        sa.Index("idx_character_name", character_name),
        sa.Index("idx_character_level", level),
    )


class CharacterLocation(Base):
    """Model for the characters location."""

    __tablename__ = "character_location"

    x: Mapped[int] = mapped_column(sa.Integer, default=0)
    y: Mapped[int] = mapped_column(sa.Integer, default=0)


class Ability(Base):
    """Model for ability."""

    __tablename__ = "ability"

    name: Mapped[str] = mapped_column(sa.String(50), unique=True)
    ability_type_id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(as_uuid=True), ForeignKey("ability_type.id", ondelete="CASCADE")
    )

    ability_type: Mapped["AbilityType"] = relationship(
        "AbilityType", foreign_keys=[ability_type_id]
    )

    __table_args__ = (
        sa.Index("idx_ability_name", name),
        sa.Index("idx_ability_type_id", ability_type_id),
    )


class ClassAbility(Base):
    """Model for class abilities."""

    __tablename__ = "class_ability"

    base_class_id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(as_uuid=True), ForeignKey("base_class.id", ondelete="CASCADE")
    )
    ability_id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(as_uuid=True), ForeignKey("ability.id", ondelete="CASCADE")
    )

    base_class: Mapped["BaseClass"] = relationship(
        "BaseClass", foreign_keys=[base_class_id]
    )
    ability: Mapped["Ability"] = relationship("Ability", foreign_keys=[ability_id])

    __table_args__ = (
        sa.Index("idx_class_ability_base_class_id", base_class_id),
        sa.Index("idx_class_ability_ability_id", ability_id),
    )


class CharacterAttribute(Base):
    """Model for character attributes."""

    __tablename__ = "character_attribute"

    character_id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(as_uuid=True), ForeignKey("character.id", ondelete="CASCADE")
    )
    attribute_id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(as_uuid=True), ForeignKey("attribute.id")
    )
    value: Mapped[int] = mapped_column(sa.Integer)

    character: Mapped["Character"] = relationship(
        "Character", foreign_keys=[character_id]
    )
    attribute: Mapped["Attribute"] = relationship(
        "Attribute", foreign_keys=[attribute_id]
    )
