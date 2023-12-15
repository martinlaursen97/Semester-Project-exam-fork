from fastapi import FastAPI
from rpg_api.db.postgres.session import AsyncSessionWrapper
from rpg_api.web.api.postgres.auth import auth_utils

from rpg_api.web.daos.base_class_dao import BaseClassDAO
from rpg_api.web.daos.place_dao import PlaceDAO
from rpg_api.web.daos.base_user_dao import BaseUserDAO
from rpg_api.utils import dtos
import sqlalchemy as sa
from rpg_api.settings import settings


async def create_startup_data_pg(app: FastAPI) -> None:  # pragma: no cover
    """Initializes the db with roles, classes, places, and users for the app."""

    # DB roles and users
    await _create_db_roles(app)

    # DB data
    # await _create_classes(app)
    # await _create_places(app)
    await _create_users(app)


async def _create_db_roles(app: FastAPI) -> None:
    """Creates and configures db roles with specific privileges for app operation."""

    session: AsyncSessionWrapper = app.state.db_session_factory()

    roles_and_passwords = [
        (settings.db_admin_user, settings.db_admin_pass),
        (settings.db_read_user, settings.db_read_pass),
        (settings.db_read_restricted_user, settings.db_read_restricted_pass),
    ]

    for role, password in roles_and_passwords:
        check_role_exists = "SELECT 1 FROM pg_roles WHERE rolname = :role"
        result = await session.execute(sa.text(check_role_exists), {"role": role})
        role_exists = result.scalar_one_or_none()

        if not role_exists:
            await session.execute(
                sa.text(f"CREATE ROLE {role} WITH LOGIN PASSWORD '{password}'"),
            )

            match role:
                case settings.db_admin_user:
                    await session.execute(
                        sa.text(
                            f"GRANT ALL PRIVILEGES ON DATABASE {settings.db_base} TO {role}"  # noqa: E501
                        ),
                    )
                case settings.db_read_user:
                    await session.execute(
                        sa.text(
                            f"GRANT SELECT ON ALL TABLES IN SCHEMA public TO {role}"
                        ),
                    )
                case settings.db_read_restricted_user:
                    await session.execute(
                        sa.text(f"GRANT SELECT ON TABLE base_user TO {role}"),
                    )

    await session.commit()


async def _create_classes(app: FastAPI) -> None:  # pragma: no cover
    """Create startup data for the postgresql database."""

    session: AsyncSessionWrapper = app.state.db_session_factory()
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


async def _create_places(app: FastAPI) -> None:  # pragma: no cover
    """Create startup data for the postgresql database."""

    session: AsyncSessionWrapper = app.state.db_session_factory()
    place_dao = PlaceDAO(session=session)

    input_places = [
        dtos.PlaceInputDTO(
            name="Goldshire", description="goldshire", radius=40, x=25, y=-100
        ),
        dtos.PlaceInputDTO(
            name="Stormwind City",
            description="stormwind city",
            radius=100,
            x=-150,
            y=50,
        ),
        dtos.PlaceInputDTO(
            name="Ironforge", description="ironforge", radius=70, x=100, y=100
        ),
    ]
    db_places = await place_dao.filter()

    for place in input_places:
        if not any([db_place.name == place.name for db_place in db_places]):
            await place_dao.create(input_dto=place)

    await session.commit()
    await session.close()


async def _create_users(app: FastAPI) -> None:  # pragma: no cover
    """Create 3 startup users for the postgresql database."""
    session: AsyncSessionWrapper = app.state.db_session_factory()
    user_dao = BaseUserDAO(session=session)

    input_users = [
        dtos.BaseUserInputDTO(
            email=f"user{i}@example.com",
            password=auth_utils.hash_password("password"),
        )
        for i in range(3)
    ]

    db_users = await user_dao.filter()

    for user in input_users:
        if not any([db_user.email == user.email for db_user in db_users]):
            await user_dao.create(input_dto=user)

    await session.commit()
    await session.close()
