from fastapi import FastAPI

from rpg_api.utils import models
from rpg_api.web.api.postgres.auth import auth_utils as utils
import random


async def create_startup_data_mongo(app: FastAPI) -> None:  # pragma: no cover
    """Create startup classes for the mongodb database."""

    await _create_abilities()
    await _create_classes()
    await _create_users()
    await _create_characters()
    await _create_places()

    await _add_friends_to_users()
    await _add_characters_to_users()


async def _create_users() -> None:  # pragma: no cover
    """Create 100 startup users for the mongodb database."""

    for i in range(100):
        email = f"mongo{i}@gmail.com"

        if await models.MBaseUser.get_by_email(email):
            continue

        new_user = models.MBaseUser(
            email=f"mongo{i}@gmail.com",
            password=utils.hash_password("password"),
        )

        await new_user.save()  # type: ignore


async def _create_abilities() -> None:  # pragma: no cover
    """Create startup abilities for the mongodb database."""

    input_abilities = [
        models.MAbility(name="Fireball", description="Fireball"),
        models.MAbility(name="Frostbolt", description="Frostbolt"),
        models.MAbility(name="Shadowbolt", description="Shadowbolt"),
        models.MAbility(name="Heal", description="Heal"),
        models.MAbility(name="Smite", description="Smite"),
        models.MAbility(name="Sinister Strike", description="Sinister Strike"),
    ]

    db_abilities: list[models.MAbility] = await models.MAbility.find_all().to_list()

    for ability in input_abilities:
        if not any([db_ability.name == ability.name for db_ability in db_abilities]):
            await ability.save()  # type: ignore


async def _create_classes() -> None:  # pragma: no cover
    """Create startup classes for the mongodb database."""

    warrior_ability = await models.MAbility.find_one({"name": "Sinister Strike"})
    mage_ability = await models.MAbility.find_one({"name": "Fireball"})
    rogue_ability = await models.MAbility.find_one({"name": "Sinister Strike"})
    priest_abilities = [
        await models.MAbility.find_one({"name": "Heal"}),
        await models.MAbility.find_one({"name": "Smite"}),
    ]

    input_classes = [
        models.MClass(
            name="Warrior",
            description="Warrior",
            abilities=[warrior_ability],  # type: ignore
        ),
        models.MClass(name="Mage", description="Mage", abilities=[mage_ability]),  # type: ignore
        models.MClass(name="Rogue", description="Rogue", abilities=[rogue_ability]),  # type: ignore
        models.MClass(name="Priest", description="Priest", abilities=priest_abilities),  # type: ignore
    ]

    db_classes = await models.MClass.find_all().to_list()

    for class_ in input_classes:
        if not any([db_class.name == class_.name for db_class in db_classes]):
            await class_.save()  # type: ignore


async def _create_characters() -> None:  # pragma: no cover
    """Create 3 characters for each user."""

    users: list[models.MBaseUser] = await models.MBaseUser.find_all().to_list()

    for user in users:
        for i in range(3):
            character_name = f"{user.email}_{i}"

            character_exists = (
                await models.MCharacter.find_one({"character_name": character_name})
                is not None
            )

            if character_exists:
                return

            class_ = await models.MClass.find_one()
            character_attributes = [
                models.EmbedAttribute(attribute=models.MAttributeType.strength),
                models.EmbedAttribute(attribute=models.MAttributeType.dexterity),
                models.EmbedAttribute(attribute=models.MAttributeType.intelligence),
            ]

            details = models.EmbedCharacterDetails(character_name=character_name)
            location = models.EmbedLocation(x=0, y=0)

            character = models.MCharacter(
                class_=class_,  # type: ignore
                character_attributes=character_attributes,
                details=details,
                location=location,
            )
            await character.save()  # type: ignore


async def _create_places() -> None:  # pragma: no cover
    """Create startup places for the mongodb database."""

    input_places = [
        models.MPlace(
            name="Goldshire",
            description="goldshire",
            radius=40,
            location=models.EmbedLocation(x=25, y=-100),
        ),
        models.MPlace(
            name="Stormwind City",
            description="stormwind city",
            radius=100,
            location=models.EmbedLocation(x=-150, y=50),
        ),
        models.MPlace(
            name="Ironforge",
            description="ironforge",
            radius=70,
            location=models.EmbedLocation(x=100, y=100),
        ),
    ]
    db_places = await models.MPlace.find_all().to_list()

    for place in input_places:
        if not any([db_place.name == place.name for db_place in db_places]):
            await place.save()  # type: ignore


async def _add_friends_to_users() -> None:  # pragma: no cover
    """Add 3-8 friends to each user."""

    users = await models.MBaseUser.find_all().to_list()
    for user in users:
        if not user.characters:
            continue
        random_indexes = random.sample(range(0, len(users)), random.randint(3, 8))
        friends = [users[i].id for i in random_indexes if users[i].id != user.id]
        await user.update({"$set": {"friends": friends}})


async def _add_characters_to_users() -> None:  # pragma: no cover
    """Add 3 characters to each user."""

    users = await models.MBaseUser.find_all().to_list()
    characters = await models.MCharacter.find_all().to_list()
    for idx, user in enumerate(users):
        if not user.friends:
            continue
        next_3_characters = characters[idx * 3 : idx * 3 + 3]
        characters_ids = [character.id for character in next_3_characters]
        await user.update({"$set": {"characters": characters_ids}})
