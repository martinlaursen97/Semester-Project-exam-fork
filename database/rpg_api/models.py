from sqlalchemy import Column, Date, ForeignKeyConstraint, Identity, Integer, PrimaryKeyConstraint, String, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class AbilityType(Base):
    __tablename__ = 'ability_type'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='ability_type_pkey'),
        UniqueConstraint('name', name='ability_type_name_key')
    )

    id = Column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1))
    name = Column(String(20), nullable=False)
    description = Column(String(200), nullable=False)
    created_at = Column(Date, nullable=False)

    ability = relationship('Ability', back_populates='ability_type')


class Ability(Base):
    __tablename__ = 'ability'
    __table_args__ = (
        ForeignKeyConstraint(['ability_type_id'], ['ability_type.id'], ondelete='CASCADE', name='fk_ability_type'),
        PrimaryKeyConstraint('id', name='ability_pkey'),
        UniqueConstraint('name', name='ability_name_key')
    )

    id = Column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1))
    name = Column(String(20), nullable=False)
    ability_type_id = Column(Integer, nullable=False)
    created_at = Column(Date, nullable=False)

    ability_type = relationship('AbilityType', back_populates='ability')
