from rpg_api.tests.pytest.test_utils import (
    gen_email,
    gen_max_length_email,
    gen_min_length_email,
    gen_string,
    EMAIL_ADDITIONAL_LENGTH,
    MAX_BEFORE_AT,
    MAX_AFTER_AT,
)
from rpg_api.utils import dtos
import pytest
from pydantic import SecretStr
from rpg_api import constants


@pytest.mark.parametrize(
    "password",
    [
        gen_string(constants.MIN_LENGTH_PASSWORD),  # Valid: 8 chars
        gen_string(constants.MIN_LENGTH_PASSWORD + 1),  # Valid: 9 chars
        gen_string(constants.MAX_LENGTH_PASSWORD // 2),  # Valid: Test value 16 chars
        gen_string(constants.MAX_LENGTH_PASSWORD),  # Valid: 32 chars
        gen_string(constants.MAX_LENGTH_PASSWORD - 1),  # Valid: 31 chars
    ],
)
def test_user_login_dto_valid_password(password: str) -> None:
    """Test UserLoginDTO password length."""

    email = "valid@email.com"

    dto = dtos.UserLoginDTO(email=email, password=SecretStr(password))

    assert dto.email == email
    assert dto.password.get_secret_value() == password


@pytest.mark.parametrize(
    "password",
    [
        gen_string(constants.MIN_LENGTH_PASSWORD - 1),  # Invalid: 7 chars
        gen_string(constants.MIN_LENGTH_PASSWORD - 2),  # Invalid: 6 chars
        gen_string(constants.MAX_LENGTH_PASSWORD + 1),  # Invalid: 33 chars
        gen_string(constants.MAX_LENGTH_PASSWORD + 2),  # Invalid: 34 chars
        gen_string(constants.MAX_LENGTH_PASSWORD + 3),  # Invalid: Test value 35 chars
        gen_string(constants.MIN_LENGTH_PASSWORD - 3),  # Invalid: Test value 5 chars
    ],
)
def test_user_login_dto_invalid_password(password: str) -> None:
    """Test UserLoginDTO password length."""

    email = "valid@email.com"

    with pytest.raises(ValueError):
        dtos.UserLoginDTO(email=email, password=SecretStr(password))


@pytest.mark.parametrize(
    "email",
    [
        gen_max_length_email(),  # Valid: 100 chars
        gen_max_length_email(-1),  # Valid: 99 chars
        gen_min_length_email(),  # Valid: 10 chars
        gen_min_length_email(1),  # Valid: 11 chars
        gen_email(
            25, 25 - EMAIL_ADDITIONAL_LENGTH
        ),  # Valid: Test value 50 chars before @
        gen_email(MAX_BEFORE_AT, 1),  # Valid: 64 chars before @
        gen_email(MAX_BEFORE_AT - 1, 1),  # Valid: 63 chars before @
        gen_email(MAX_BEFORE_AT // 2, 1),  # Valid: Test value 32 chars before @
        gen_email(1, MAX_AFTER_AT),  # Valid: 63 chars after @
        gen_email(1, MAX_AFTER_AT - 1),  # Valid: 62 chars after @
        gen_email(1, MAX_AFTER_AT // 2),  # Valid: Test value 31 chars after @
    ],
)
def test_user_login_dto_valid_email(email: str) -> None:
    """Test UserLoginDTO email length."""

    password = "password"

    dto = dtos.UserLoginDTO(email=email, password=SecretStr(password))

    assert dto.email == email
    assert dto.password.get_secret_value() == password


@pytest.mark.parametrize(
    "email",
    [
        gen_max_length_email(1),  # Invalid: 101 chars
        gen_max_length_email(2),  # Invalid: 102 chars
        gen_max_length_email(5),  # Invalid: Test value 105 chars
        gen_min_length_email(-1),  # Invalid: 9 chars
        gen_min_length_email(-2),  # Invalid: 8 chars
        gen_min_length_email(-5),  # Invalid: Test value 5 chars
        gen_email(MAX_BEFORE_AT + 1, 1),  # Invalid: 65 chars before @
        gen_email(MAX_BEFORE_AT + 2, 1),  # Invalid: 66 chars before @
        gen_email(MAX_BEFORE_AT + 6, 1),  # Invalid: Test value 70 chars before @
        gen_email(1, MAX_AFTER_AT + 1),  # Invalid: 64 chars after @
        gen_email(1, MAX_AFTER_AT + 2),  # Invalid: 65 chars after @
        gen_email(1, MAX_AFTER_AT + 7),  # Invalid: Test value 70 chars after @
    ],
)
def test_user_login_dto_invalid_email(email: str) -> None:
    """Test UserLoginDTO email length."""

    password = "password"

    with pytest.raises(ValueError):
        dtos.UserLoginDTO(email=email, password=SecretStr(password))
