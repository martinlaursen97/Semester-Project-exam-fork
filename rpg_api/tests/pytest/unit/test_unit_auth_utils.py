import pytest
from rpg_api.web.api.postgres.auth.auth_utils import (
    hash_password,
    verify_password,
)


def test_hash_password() -> None:
    """Test hash_password hashes the password."""
    password = "password"

    hashed_password = hash_password(password)

    assert hashed_password != password
    assert hashed_password is not None


def test_hash_password_always_different_hash() -> None:
    """Test that hash_password always returns a different hash."""
    password = "password"

    hashed_password1 = hash_password(password)
    hashed_password2 = hash_password(password)

    assert hashed_password1 != hashed_password2


def test_hash_password_with_null_input() -> None:
    """Test hashing with a None input."""
    with pytest.raises(TypeError):
        hash_password(None)  # type: ignore[arg-type]


def test_hash_password_format() -> None:
    """Test hashing with a None input."""
    password = "password"

    hashed_password = hash_password(password)

    assert hashed_password.startswith("$2b$")


def test_hash_password_above_72_chars() -> None:
    """
    Test hashing with a password above 72 characters.
    bcrypt only hashes the first 72 characters and ignores the rest.
    As it ignores anything past 72, the verify_password function
    will return True for both passwords.
    """
    password_to_be_hashed = "a" * 72
    extended_password_to_be_hashed = password_to_be_hashed + "b"

    hashed_password = hash_password(password_to_be_hashed)
    extended_hashed_password = hash_password(extended_password_to_be_hashed)
    password = verify_password(password_to_be_hashed, hashed_password)
    extended_password = verify_password(password_to_be_hashed, extended_hashed_password)

    assert password == extended_password
    assert password is True
    assert extended_password is True


@pytest.mark.parametrize(
    "pw",
    [
        "",
        "a" * 72,
        "!@#$%^&*()",
        "باسورد",
        "пассворд",
        "πάσσωορδ",
        "פסוורד",
        "पासवर्ड",
        "パスワード",
        "密码",
        "패스워드",
        "պասվորդ",
        "პასვორდი",
    ],
)
def test_hash_and_verify_password_edge_cases(pw: str) -> None:
    """Test hashing with edge case passwords and different languages."""
    password = pw

    hashed_password = hash_password(password)
    verified_password = verify_password(password, hashed_password)

    assert hashed_password is not None
    assert hashed_password != password
    assert verified_password is True


def test_verify_password() -> None:
    """Test verify_password verifies the password correctly."""
    password = "password"
    different_password = "different_password"
    hashed_password = hash_password(password)

    verified_password = verify_password(password, hashed_password)
    wrong_password = verify_password(different_password, hashed_password)

    assert verified_password is True
    assert wrong_password is False


def test_verify_password_with_null_input() -> None:
    """Test hashing with a None input."""
    password = "password"
    hashed_password = hash_password(password)

    with pytest.raises(TypeError):
        verify_password(None, hashed_password)  # type: ignore[arg-type]
        verify_password(password, None)  # type: ignore[arg-type]
