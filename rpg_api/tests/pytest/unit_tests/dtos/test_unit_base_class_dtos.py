import pytest
from pydantic import ValidationError
from uuid import uuid4
from rpg_api.utils import dtos
from typing import Any


def test_base_class_dto_valid_input() -> None:
    """Test base class dto, with valid input."""
    valid_id = uuid4()
    valid_name = "Test Name"
    dto = dtos.BaseClassDTO(id=valid_id, name=valid_name)
    assert dto.id == valid_id
    assert dto.name == valid_name


@pytest.mark.parametrize(
    "invalid_id",
    [
        "not-a-uuid",
        123456,  # Integer
        None,  # Null value
        True,  # Boolean value
        1.0,  # double
        "",  # Empty string
        "g1234567-g89b-12d3-a456-426614174000",  # Invalid UUID characters
        "123e4567-e89b-12d3-a456-42661417400",  # Short one character
        "123e4567-e89b-12d3-a456-4266141740000",  # One character too long
        "1" * 36,  # String of 36 characters
        "-123e4567-e89b-12d3-a456-426614174000",  # Starting with a hyphen
        "123e4567-e89b-12d3-a456-",  # Missing part of the UUID
        "123e4567-e89b-12d3-a456-42661",  # Incomplete UUID
        "123e4567-e89b-12d3-a456-426614174000-426614174000",  # Double UUID
        "123e4567-e89b-12d3-a456-42661417400z",  # Non-hex character at the end
    ],
)
def test_base_class_dto_invalid_id(invalid_id: Any) -> None:
    """
    Test base class raises ValidationError, if id is not the correct format or type.
    """

    valid_name = "Test Name"

    with pytest.raises(ValidationError):
        dtos.BaseClassDTO(id=invalid_id, name=valid_name)


@pytest.mark.parametrize(
    "invalid_name",
    [
        123,  # Integer
        None,  # Null value
        True,  # Boolean
        1.0,  # Floating point number
    ],
)
def test_base_class_dto_invalid_name(invalid_name: Any) -> None:
    """Test base class raises ValidationError, if class name is not the correct type."""

    valid_id = uuid4()

    with pytest.raises(ValidationError):
        dtos.BaseClassDTO(id=valid_id, name=invalid_name)
