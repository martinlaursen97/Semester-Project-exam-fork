from rpg_api.utils import dtos
import pytest
from pydantic import SecretStr
from rpg_api import constants

email_additional_length = len("@.com")
max_before_at = 64
max_after_at = 63


def _gen_email(before_at: int, after_at: int) -> str:
    """Generate an email of a given length before and after the @."""
    return f"{'a' * before_at}@{'b' * after_at}.com"


def _gen_max_length_email(extra: int = 0) -> str:
    """Generate an email of maximum length."""
    extra += 1 if constants.MAX_LENGTH_EMAIL % 2 else 0
    return _gen_email(
        constants.MAX_LENGTH_EMAIL // 2 + extra,
        constants.MAX_LENGTH_EMAIL // 2 - email_additional_length,
    )


def _gen_string(length: int) -> str:
    """Generate a string of a given length."""
    return f"{'a' * length}"


@pytest.mark.parametrize(
    "password",
    [
        _gen_string(constants.MIN_LENGTH_PASSWORD),
        _gen_string(constants.MIN_LENGTH_PASSWORD + 1),
        _gen_string(constants.MAX_LENGTH_PASSWORD // 2),
        _gen_string(constants.MAX_LENGTH_PASSWORD),
        _gen_string(constants.MAX_LENGTH_PASSWORD - 1),
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
        _gen_string(constants.MIN_LENGTH_PASSWORD - 1),
        _gen_string(constants.MIN_LENGTH_PASSWORD - 2),
        _gen_string(constants.MAX_LENGTH_PASSWORD + 1),
        _gen_string(constants.MAX_LENGTH_PASSWORD + 2),
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
        _gen_max_length_email(),
        _gen_max_length_email(-1),
        _gen_email(max_before_at, 1),
        _gen_email(max_before_at - 1, 1),
        _gen_email(1, max_after_at),
        _gen_email(1, max_after_at - 1),
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
        _gen_max_length_email(1),
        _gen_max_length_email(2),
        _gen_email(max_before_at + 1, 1),
        _gen_email(max_before_at + 2, 1),
        _gen_email(1, max_after_at + 1),
        _gen_email(1, max_after_at + 2),
    ],
)
def test_user_login_dto_invalid_email(email: str) -> None:
    """Test UserLoginDTO email length."""

    password = "password"

    with pytest.raises(ValueError):
        dtos.UserLoginDTO(email=email, password=SecretStr(password))
