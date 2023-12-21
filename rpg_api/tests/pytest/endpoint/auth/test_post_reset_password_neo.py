import pytest
from httpx import AsyncClient
from fastapi import status
from rpg_api.utils import dtos
from rpg_api.utils.daos import AllDAOs
from rpg_api.web.api.neo4j.auth.token_store import token_store
from rpg_api.web.api.postgres.auth import auth_utils as utils
from rpg_api import constants
from uuid import uuid4
from rpg_api.db.postgres.factory import factories
from rpg_api.web.daos.base_user_dao import NeoBaseUserDAO
from neo4j import AsyncSession

url = "/api/neo4j/auth/reset-password"


@pytest.mark.anyio
@pytest.mark.parametrize(
    "new_password",
    # Valid equivalence classes
    [
        # Boundary values -> valid = (>= min and <= max)
        "a" * constants.MIN_LENGTH_PASSWORD,  # Minimum length (Lower bound)
        "a" * (constants.MIN_LENGTH_PASSWORD + 1),  # Minimum length + 1
        "a" * (constants.MAX_LENGTH_PASSWORD // 2),  # Middle length
        "a" * (constants.MAX_LENGTH_PASSWORD - 1),  # Maximum length - 1
        "a" * constants.MAX_LENGTH_PASSWORD,  # Maximum length (Upper bound)
        # Normal values
        "12!@AB$c{x",  # Password with special characters
        "with space",  # Password with spaces
        "1234567890",  # Password with only numbers
        "MiXtUrE???",  # Password with a mixture of uppercase and lowercase letters
        "UPPERCASEX",  # Password with all uppercase letters
        "lowercasex",  # Password with all lowercase letters
    ],
)
async def test_reset_password(
    new_password: str,
    client: AsyncClient,
    neo4j_session: AsyncSession,
) -> None:
    """Test reset password: 200."""

    user_input = dtos.NeoBaseUserDTO(email="test@email.com", password="password")
    user_dao = NeoBaseUserDAO(session=neo4j_session)

    user_id = await user_dao.create(input_dto=user_input)

    # Create a token and store it in the token store
    token = utils.create_reset_password_token(
        data=dtos.TokenData(
            user_id=str(user_id),
        )
    )
    token_store.set(user_id=user_id, token=token)

    response = await client.post(
        url, json={"token": token, "new_password": new_password}
    )
    assert response.status_code == status.HTTP_200_OK

    # Check that the token was removed from the token store
    assert token_store.get(user_id=user_id) is None

    # Check that the password was updated
    db_user = await user_dao.get_by_id(node_id=int(user_id))
    assert db_user is not None
    assert utils.verify_password(new_password, db_user.password)


# @pytest.mark.anyio
# @pytest.mark.parametrize(
#     "token, error_msg",
#     [
#         ("invalid_token", "Invalid token"),  # Invalid token (decoding fails)
#         (
#             utils.create_reset_password_token(  # Invalid token (user_id does not exist)
#                 data=dtos.TokenData(
#                     user_id=str(uuid4()),
#                 )
#             ),
#             "user does not exist",
#         ),
#     ],
# )
# async def test_reset_password_invalid_token(
#     token: str,
#     error_msg: str,
#     client: AsyncClient,
# ) -> None:
#     """Test reset password when token is invalid: 401."""

#     response = await client.post(
#         url, json={"token": token, "new_password": "new_password"}
#     )
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
#     assert error_msg in response.json()["detail"]


# @pytest.mark.anyio
# async def test_reset_password_token_already_used(
#     client: AsyncClient,
# ) -> None:
#     """Test reset password when token has already been used: 401."""

#     user = await factories.BaseUserFactory.create()

#     # Create a token and store it in the token store
#     token = utils.create_reset_password_token(
#         data=dtos.TokenData(
#             user_id=str(user.id),
#         )
#     )
#     token_store.set(user_id=user.id, token=token)

#     # Use the token once
#     response = await client.post(
#         url, json={"token": token, "new_password": "new_password"}
#     )
#     assert response.status_code == status.HTTP_200_OK

#     # Use the token again
#     response = await client.post(
#         url, json={"token": token, "new_password": "new_password"}
#     )
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
#     assert "already been used" in response.json()["detail"]


# @pytest.mark.anyio
# @pytest.mark.parametrize(
#     "new_password",
#     # Invalid equivalence classes
#     [
#         "a" * (constants.MIN_LENGTH_PASSWORD - 1),  # Minimum length - 1 (Lower bound)
#         "a" * (constants.MAX_LENGTH_PASSWORD + 1),  # Maximum length + 1 (Upper bound)
#         "",
#         0,
#         None,
#         True,
#     ],
# )
# async def test_reset_password_invalid_input(
#     new_password: str,
#     client: AsyncClient,
# ) -> None:
#     """Test reset password when input is invalid: 422."""

#     user = await factories.BaseUserFactory.create()

#     # Create a token and store it in the token store
#     token = utils.create_reset_password_token(
#         data=dtos.TokenData(
#             user_id=str(user.id),
#         )
#     )
#     token_store.set(user_id=user.id, token=token)

#     response = await client.post(
#         url, json={"token": token, "new_password": new_password}
#     )
#     assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
