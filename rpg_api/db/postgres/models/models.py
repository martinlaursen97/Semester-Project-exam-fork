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

    first_name: Mapped[str | None] = mapped_column(sa.String(50), default=None)
    last_name: Mapped[str | None] = mapped_column(sa.String(50), default=None)
    email: Mapped[str] = mapped_column(sa.String(100), unique=True)
    phone: Mapped[str | None] = mapped_column(sa.String(20), default=None)
    password: Mapped[str] = mapped_column(sa.String(255))
    status: Mapped[UserStatus] = mapped_column(
        sa.Enum(UserStatus, name="user_status"), default=UserStatus.active
    )

    # relations: Mapped[list["Relation"]] = relationship()
    # characters: Mapped[list["Character"]] = relationship()


class AbilityType(Base):
    """Ability type model."""

    __tablename__ = "ability_type"

    name: Mapped[str] = mapped_column(sa.String(50))
    description: Mapped[str] = mapped_column(sa.String(500))
    abilities: Mapped[list["Ability"]] = relationship()


class BaseClass(Base):
    """Model for base class."""

    __tablename__ = "base_class"

    name: Mapped[str] = mapped_column(sa.String(50))
    # characters: Mapped[list["Character"]] = relationship()
    # class_abilities: Mapped[list["ClassAbility"]] = relationship()


class Attribute(Base):
    """Model for Attribute."""

    __tablename__ = "attribute"

    name: Mapped[str] = mapped_column(sa.String(50))
    description: Mapped[str] = mapped_column(sa.String(500))

    character_attributes: Mapped[list["CharacterAttribute"]] = relationship()


class Place(Base):
    """Model for place."""

    __tablename__ = "place"

    name: Mapped[str] = mapped_column(sa.String(50))
    radius: Mapped[int] = mapped_column(sa.Integer)
    x: Mapped[int] = mapped_column(sa.Integer)
    y: Mapped[int] = mapped_column(sa.Integer)


class Relation(Base):
    """Model for relations."""

    __tablename__ = "relation"

    user1_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("base_user.id"))
    user2_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("base_user.id"))


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
    character_name: Mapped[str] = mapped_column(sa.String(50))
    alive: Mapped[bool] = mapped_column(sa.Boolean, default=True)
    level: Mapped[int] = mapped_column(sa.Integer, default=1)
    xp: Mapped[int] = mapped_column(sa.Integer, default=1)
    money: Mapped[int] = mapped_column(sa.Integer, default=1)

    base_class: Mapped["BaseClass"] = relationship(
        "BaseClass", foreign_keys=[base_class_id]
    )
    user: Mapped["BaseUser"] = relationship("BaseUser", foreign_keys=[user_id])
    character_location: Mapped["CharacterLocation | None"] = relationship(
        "CharacterLocation",
        foreign_keys=[character_location_id],
        uselist=False,
    )


class CharacterLocation(Base):
    """Model for the characters location."""

    __tablename__ = "character_location"

    x: Mapped[int] = mapped_column(sa.Integer, default=0)
    y: Mapped[int] = mapped_column(sa.Integer, default=0)


class Ability(Base):
    """Model for ability."""

    __tablename__ = "ability"

    name: Mapped[str] = mapped_column(sa.String(50))
    ability_type_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ability_type.id"))

    class_ability: Mapped[list["ClassAbility"]] = relationship()


class ClassAbility(Base):
    """Model for class abilities."""

    __tablename__ = "class_ability"

    base_class_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("base_class.id"))
    ability_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ability.id"))


class CharacterAttribute(Base):
    """Model for character attributes ."""

    __tablename__ = "character_attributes"

    character_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("character.id"))
    attribute_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("attribute.id"))
    value: Mapped[int] = mapped_column(sa.Integer)
