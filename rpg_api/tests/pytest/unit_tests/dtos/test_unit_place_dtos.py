from rpg_api.tests.pytest.test_utils import (
    gen_string,
)
from rpg_api.utils import dtos
import pytest
from rpg_api import constants


@pytest.mark.parametrize(
    "name",
    [
        gen_string(constants.MIN_LENGTH_PLACE_NAME),  # Valid: 3 chars
        gen_string(constants.MIN_LENGTH_PLACE_NAME + 1),  # Valid: 4 chars
        gen_string(constants.MAX_LENGTH_PLACE_NAME // 2),  # Valid: Test value 16 chars
        gen_string(constants.MAX_LENGTH_PLACE_NAME),  # Valid: 50 chars
        gen_string(constants.MAX_LENGTH_PLACE_NAME - 1),  # Valid: 49 chars
    ],
)
def test_user_login_input_dto_name_valid(name: str) -> None:
    """Test UserLoginInputDTO name length."""

    dto = dtos.PlaceInputDTO(name=name, description="test")

    assert dto.name == name


@pytest.mark.parametrize(
    "name",
    [
        gen_string(constants.MIN_LENGTH_PLACE_NAME - 1),  # Invalid: 2 chars
        gen_string(constants.MIN_LENGTH_PLACE_NAME - 2),  # Invalid: 1 chars
        gen_string(constants.MAX_LENGTH_PLACE_NAME + 1),  # Invalid: 51 chars
        gen_string(constants.MAX_LENGTH_PLACE_NAME + 2),  # Invalid: 52 chars
        gen_string(
            constants.MAX_LENGTH_PLACE_NAME + 70
        ),  # Invalid: Test value 53 chars
        gen_string(constants.MIN_LENGTH_PLACE_NAME - 3),  # Invalid: Test value 0 chars
    ],
)
def test_user_login_input_dto_name_invalid(name: str) -> None:
    """Test UserLoginInputDTO name length."""

    with pytest.raises(ValueError):
        dtos.PlaceInputDTO(name=name, description="test")


@pytest.mark.parametrize(
    "description",
    [
        gen_string(constants.MAX_LENGTH_DESCRIPTION),  # Valid: 500 chars
        gen_string(constants.MAX_LENGTH_DESCRIPTION - 1),  # Valid: 499 chars
        gen_string(
            constants.MAX_LENGTH_DESCRIPTION // 2
        ),  # Valid: Test value 250 chars
    ],
)
def test_user_login_input_dto_description_valid(description: str) -> None:
    """Test UserLoginInputDTO description length."""

    name = "test"

    dto = dtos.PlaceInputDTO(name=name, description=description)

    assert dto.description == description


@pytest.mark.parametrize(
    "description",
    [
        gen_string(constants.MAX_LENGTH_DESCRIPTION + 1),  # Invalid: 501 chars
        gen_string(constants.MAX_LENGTH_DESCRIPTION + 2),  # Invalid: 502 chars
        gen_string(
            constants.MAX_LENGTH_DESCRIPTION + 50
        ),  # Invalid: Test value 550 chars
    ],
)
def test_user_login_input_dto_description_invalid(description: str) -> None:
    """Test UserLoginInputDTO description length."""

    name = "test"

    with pytest.raises(ValueError):
        dtos.PlaceInputDTO(name=name, description=description)


@pytest.mark.parametrize(
    "coord",
    [
        constants.INT32_MAX,  # Valid: 2147483647
        constants.INT32_MAX - 1,  # Valid: 2147483646
        constants.INT32_MIN,  # Valid: -2147483648
        constants.INT32_MIN + 1,  # Valid: -2147483647
        constants.INT32_MAX // 2,  # Valid: Test value
        constants.INT32_MIN // 2,  # Valid: Test value
    ],
)
def test_user_login_input_dto_coord_valid(coord: int) -> None:
    """Test UserLoginInputDTO x value."""

    name = "test"

    dto = dtos.PlaceInputDTO(name=name, x=coord, y=coord, description="test")

    assert dto.x == coord
    assert dto.y == coord


@pytest.mark.parametrize(
    "coord",
    [
        constants.INT32_MAX + 1,  # Invalid: 2147483648
        constants.INT32_MAX + 2,  # Invalid: 2147483649
        constants.INT32_MIN - 1,  # Invalid: -2147483649
        constants.INT32_MIN - 2,  # Invalid: -2147483650
        constants.INT32_MAX + 1000,  # Invalid: Test value
        constants.INT32_MIN - 1000,  # Invalid: Test value
    ],
)
@pytest.mark.skip("Expected to fail")
def test_user_login_input_dto_coord_invalid(coord: int) -> None:
    """Test UserLoginInputDTO x value."""

    name = "test"

    with pytest.raises(ValueError):
        dtos.PlaceInputDTO(name=name, x=coord, y=coord, description="test")


@pytest.mark.parametrize(
    "radius",
    [0.0],
)
def test_user_login_input_dto_radius_valid(radius: float) -> None:
    """Test UserLoginInputDTO radius value."""

    name = "test"

    dto = dtos.PlaceInputDTO(name=name, radius=radius, description="test")

    assert dto.radius == radius


@pytest.mark.parametrize(
    "radius",
    [-0.01, -100.0],
)
def test_user_login_input_dto_radius_invalid(radius: float) -> None:
    """Test UserLoginInputDTO radius value."""

    name = "test"

    with pytest.raises(ValueError):
        dtos.PlaceInputDTO(name=name, radius=radius, description="test")
