import pytest
from pydantic import ValidationError
from uuid import uuid4
from rpg_api.utils import dtos
from rpg_api.enums import Gender
from typing import Any


def test_character_input_dto_valid_inputs() -> None:
    """
    Check that Character DTO gets created correctly.

    Default values are also checked:
    alive: true
    level: 1
    xp: 1
    money: 1
    """

    base_class_id = uuid4()
    user_id = uuid4()
    gender = Gender.female
    character_name = "Moshizzle"
    alive = True
    level = 1
    xp = 1
    money = 1

    character = dtos.CharacterInputDTO(
        base_class_id=base_class_id,
        user_id=user_id,
        gender=gender,
        character_name=character_name,
    )

    assert character.base_class_id == base_class_id
    assert character.user_id == user_id
    assert character.gender == gender
    assert character.character_name == character_name
    assert character.alive == alive
    assert character.level == level
    assert character.xp == xp
    assert character.money == money


@pytest.mark.parametrize(
    "invalid_uuid",
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
def test_character_input_dto_invalid_user_uuids(invalid_uuid: Any) -> None:
    """Test invalid uuid for user_id, should raise ValidationError."""
    with pytest.raises(ValidationError):
        dtos.CharacterInputDTO(
            base_class_id=uuid4(),
            user_id=invalid_uuid,
            gender=Gender.female,
            character_name="Valid Name",
        )


@pytest.mark.parametrize(
    "invalid_uuid",
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
def test_character_input_dto_invalid_base_class_uuids(invalid_uuid: Any) -> None:
    """Test invalid uuid for base_class_id, should raise ValidationError."""

    with pytest.raises(ValidationError):
        dtos.CharacterInputDTO(
            base_class_id=invalid_uuid,
            user_id=uuid4(),
            gender=Gender.male,
            character_name="Valid Name",
        )


@pytest.mark.parametrize(
    "invalid_gender", ["invalid", 123, None, "", "fema", "mal", 1.0, True]
)
def test_character_input_dto_invalid_gender(invalid_gender: Any) -> None:
    """Test invalid gender, should raise ValidationError"""
    with pytest.raises(ValidationError):
        dtos.CharacterInputDTO(
            base_class_id=uuid4(),
            user_id=uuid4(),
            gender=invalid_gender,
            character_name="Valid Name",
        )


# Test invalid character names
@pytest.mark.parametrize(
    "invalid_name",
    [
        "",# Empty name
        "a" * 51, # Long name
        1, # integer 
        None,  # Null value
        True,  # Boolean
        1.0,  # Floating point number
    ],
)
def test_character_input_dto_invalid_name(invalid_name: Any) -> None:
    with pytest.raises(ValidationError):
        dtos.CharacterInputDTO(
            base_class_id=uuid4(),
            user_id=uuid4(),
            gender=Gender.male,
            character_name=invalid_name,
        )
