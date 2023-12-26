import pytest
from rpg_api.db.postgres.factory import factories
from rpg_api.utils.daos import AllDAOs
import sqlalchemy as sa
from sqlalchemy import orm
from rpg_api.utils import models
from rpg_api.db.postgres.session import AsyncSessionWrapper

CREATE_NUM = 3


@pytest.mark.anyio
async def test_factory_base_user(daos: AllDAOs) -> None:
    """Test factory can create base users."""

    await factories.BaseUserFactory.create_batch(size=CREATE_NUM)

    db_users = await daos.base_user.filter()
    assert len(db_users) == CREATE_NUM


@pytest.mark.anyio
async def test_ability_type_factory(dbsession: AsyncSessionWrapper) -> None:
    """Test factory can create ability types."""

    await factories.AbilityTypeFactory.create_batch(size=CREATE_NUM)

    result = await dbsession.execute(sa.select(models.AbilityType))
    rows = result.all()
    assert len(rows) == 3


@pytest.mark.anyio
async def test_base_class_factory(daos: AllDAOs) -> None:
    """Test factory can create base classes."""

    await factories.BaseClassFactory.create_batch(size=CREATE_NUM)

    db_base_classes = await daos.base_class.filter()
    assert len(db_base_classes) == CREATE_NUM


@pytest.mark.anyio
async def test_attribute_factory(dbsession: AsyncSessionWrapper) -> None:
    """Test factory can create attributes."""

    await factories.AttributeFactory.create_batch(size=CREATE_NUM)

    result = await dbsession.execute(sa.select(models.Attribute))
    rows = result.all()
    assert len(rows) == CREATE_NUM


@pytest.mark.anyio
async def test_place_factory(daos: AllDAOs) -> None:
    """Test factory can create places."""

    await factories.PlaceFactory.create()

    db_places = await daos.place.filter()
    assert len(db_places) == 1


@pytest.mark.anyio
async def test_relation_factory(
    dbsession: AsyncSessionWrapper,
    daos: AllDAOs,
) -> None:
    """Test factory can create relations."""

    relation = await factories.RelationFactory.create()

    query = sa.select(models.Relation).where(
        models.Relation.id == relation.id,
    )
    loads = [
        orm.joinedload(models.Relation.user1),
        orm.joinedload(models.Relation.user2),
    ]
    for load in loads:
        query = query.options(load)

    result = await dbsession.execute(query)
    db_relation = result.scalar_one()

    assert db_relation == relation

    assert db_relation.user1 is not None
    assert db_relation.user2 is not None

    assert len(await daos.base_user.filter()) == 2


@pytest.mark.anyio
async def test_character_factory(daos: AllDAOs) -> None:
    """Test factory can create characters."""

    await factories.CharacterFactory.create_batch(size=CREATE_NUM)

    db_characters = await daos.character.filter(
        loads=[
            orm.joinedload(models.Character.base_class),
            orm.joinedload(models.Character.user),
            orm.joinedload(models.Character.character_location),
        ]
    )
    assert len(db_characters) == CREATE_NUM

    for character in db_characters:
        assert character.base_class is not None
        assert character.user is not None
        assert character.character_location is not None


@pytest.mark.anyio
async def test_character_location_factory(daos: AllDAOs) -> None:
    """Test factory can create character locations."""

    await factories.CharacterLocationFactory.create_batch(size=CREATE_NUM)

    db_character_locations = await daos.character_location.filter()
    assert len(db_character_locations) == CREATE_NUM


@pytest.mark.anyio
async def test_class_ability_factory(daos: AllDAOs) -> None:
    """Test factory can create class abilities."""

    await factories.ClassAbilityFactory.create(
        ability=await factories.AbilityFactory.create(),
    )

    query = sa.select(sa.func.count(models.ClassAbility.id))
    result = await daos.session.execute(query)

    assert result.scalar_one() == 1
