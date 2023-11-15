from fastapi import FastAPI
from rpg_api.enums import Gender

from rpg_api.web.daos.base_class_dao import BaseClassDAO
from rpg_api.web.daos.character_location_dao import CharacterLocationDAO
from rpg_api.web.daos.place_dao import PlaceDAO
from rpg_api.web.daos.base_user_dao import BaseUserDAO
from rpg_api.web.daos.base_character_dao import BaseCharacterDAO
from rpg_api.utils import dtos
import random


async def create_startup_data_pg(app: FastAPI) -> None:  # pragma: no cover
    """Create startup classes for the postgresql database."""

    await _create_startup_classes(app)
    await _create_startup_places(app)
    await _create_startup_users(app)
    await _create_startup_characters(app)
    # await _create_startup_character_locations(app)


async def _create_startup_classes(app: FastAPI) -> None:  # pragma: no cover
    """Create startup data for the postgresql database."""

    session = app.state.db_session_factory()
    base_class_dao = BaseClassDAO(session=session)

    input_classes = [
        dtos.BaseClassInputDTO(name="Warrior"),
        dtos.BaseClassInputDTO(name="Mage"),
        dtos.BaseClassInputDTO(name="Shaman"),
    ]
    db_classes = await base_class_dao.filter()

    for class_ in input_classes:
        if not any([db_class.name == class_.name for db_class in db_classes]):
            await base_class_dao.create(input_dto=class_)

    await session.commit()
    await session.close()


async def _create_startup_places(app: FastAPI) -> None:  # pragma: no cover
    """Create startup data for the postgresql database."""

    session = app.state.db_session_factory()
    place_dao = PlaceDAO(session=session)

    input_places = [
        dtos.PlaceInputDTO(name="Goldshire", radius=40, x=25, y=-100),
        dtos.PlaceInputDTO(name="Stormwind City", radius=100, x=-150, y=50),
        dtos.PlaceInputDTO(name="Ironforge", radius=70, x=100, y=100),
    ]
    db_places = await place_dao.filter()

    for place in input_places:
        if not any([db_place.name == place.name for db_place in db_places]):
            await place_dao.create(input_dto=place)

    await session.commit()
    await session.close()


async def _create_startup_users(app: FastAPI) -> None:  # pragma: no cover
    """Create 3 startup users for the postgresql database."""
    session = app.state.db_session_factory()
    user_dao = BaseUserDAO(session=session)
    try:
        input_users = [
            dtos.BaseUserInputDTO(
                email=f"user{i}@example.com",
                password="password",
                first_name="John",
                last_name="Doe",
                phone="123456789",
            )
            for i in range(3)
        ]

        db_users = await user_dao.filter()

        for user in input_users:
            if not any([db_user.email == user.email for db_user in db_users]):
                await user_dao.create(input_dto=user)
    finally:
        await session.commit()
        await session.close()


async def _create_startup_characters(app: FastAPI) -> None:  # pragma: no cover
    """Create startup characters for all users."""
    session = app.state.db_session_factory()

    character_dao = BaseCharacterDAO(session=session)
    user_dao = BaseUserDAO(session=session)
    class_dao = BaseClassDAO(session=session)

    db_users = await user_dao.filter()
    db_classes = await class_dao.filter()

    for user in db_users:
        for class_ in db_classes:
            input_character = dtos.BaseCharacterInputDTO(
                base_class_id=class_.id,
                user_id=user.id,
                gender=random.choice(list(Gender)),
                character_name=f"{class_.name} {user.first_name}",
            )
            await character_dao.create(input_dto=input_character)

    await session.commit()
    await session.close()


async def _create_startup_character_locations(app: FastAPI) -> None:  # pragma: no cover
    """Create startup character locations for all characters."""

    session = app.state.db_session_factory()
    character_location_dao = CharacterLocationDAO(session=session)
    character_dao = BaseCharacterDAO(session=session)

    db_characters = await character_dao.filter()

    for character in db_characters:
        input_character_location = dtos.CharacterLocationInputDTO(
            base_character_id=character.id,
            x=random.randint(-200, 200),
            y=random.randint(-200, 200),
        )
        await character_location_dao.create(input_dto=input_character_location)

    await session.commit()
    await session.close()
