from datetime import datetime
from rpg_api.utils import dtos
import pytest
from rpg_api.enums import UserStatus
from uuid import uuid4


@pytest.mark.parametrize(
    "status",
    [
        UserStatus.active,
        UserStatus.inactive,
        "active",
        "inactive",
    ],
)
def test_base_user_dto_status_valid(status: UserStatus) -> None:
    """Test BaseUserDTO."""

    id = uuid4()
    email = "test@email.com"
    created_at = datetime.now()

    dto = dtos.BaseUserDTO(
        id=id,
        email=email,
        status=status,
        created_at=created_at,
    )

    assert dto.id == id
    assert dto.email == email
    assert dto.status == status
    assert dto.created_at == created_at


@pytest.mark.parametrize(
    "status",
    [
        0,
        False,
        None,
        "invalid",
    ],
)
def test_base_user_dto_status_invalid(status: UserStatus) -> None:
    """Test BaseUserDTO."""

    id = uuid4()
    email = "test@email.com"
    created_at = datetime.now()

    with pytest.raises(ValueError):
        dtos.BaseUserDTO(
            id=id,
            email=email,
            status=status,
            created_at=created_at,
        )


def test_base_user_input_dto() -> None:
    """Test BaseUserInputDTO."""

    email = "test@email.com"
    password = "password"

    dto = dtos.BaseUserInputDTO(
        email=email,
        password=password,
    )

    assert dto.email == email
    assert dto.password == password
    assert dto.status == UserStatus.active  # default


def test_base_user_update_dto() -> None:
    """Test BaseUserUpdateDTO."""

    dto = dtos.BaseUserUpdateDTO()

    # default values
    assert dto.email is None
    assert dto.password is None
