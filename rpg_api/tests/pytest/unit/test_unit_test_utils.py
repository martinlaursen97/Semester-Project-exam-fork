import pytest
import uuid
from httpx import Response
from unittest.mock import patch
from rpg_api.tests.pytest.test_utils import get_user_header, get_data
import jwt


def test_get_user_header_valid_user_id() -> None:
    """
    Test that get_user_header returns the correct header,
    when provided with a valid user_id.
    """
    user_id = uuid.uuid4()
    expected_token = "test_token"
    expected_header = {"Authorization": f"Bearer {expected_token}"}

    with (
        patch("rpg_api.utils.dtos.TokenData") as mock_token_data,
        patch(
            "rpg_api.web.api.postgres.auth.auth_utils.create_access_token",
            return_value="test_token",
        ),
    ):
        header = get_user_header(user_id)

        mock_token_data.assert_called_with(user_id=str(user_id))
        assert header == expected_header


def test_get_user_header_no_user_id() -> None:
    """
    Test that the get_user_header generates a valid id,
    when no user_id is provided.
    """
    user_id = uuid.uuid4()
    expected_token = "test_token"
    expected_header = {"Authorization": f"Bearer {expected_token}"}

    with (
        patch("uuid.uuid4", return_value=user_id) as mock_id,
        patch("rpg_api.utils.dtos.TokenData") as mock_token_data,
        patch(
            "rpg_api.web.api.postgres.auth.auth_utils.create_access_token",
            return_value="test_token",
        ),
    ):
        header = get_user_header()

        mock_id.assert_called_once()
        mock_token_data.assert_called_with(user_id=str(user_id))
        assert header == expected_header


def test_get_user_header_invalid_user_id() -> None:
    """
    Test that get_user_header raises a TypeError
    when provided with an invalid user_id.
    """
    with pytest.raises(TypeError):
        get_user_header(user_id="not-a-uuid")  # type: ignore[arg-type]


def test_get_user_header_token_creation_failure() -> None:
    """
    Test that get_user_header raises an PyJWTError
    when access token creation fails.
    """
    with (
        patch("rpg_api.utils.dtos.TokenData"),
        patch(
            "rpg_api.web.api.postgres.auth.auth_utils.create_access_token",
            side_effect=jwt.exceptions.PyJWTError,
        ),
    ):
        with pytest.raises(jwt.exceptions.PyJWTError):
            get_user_header()


def test_get_data() -> None:
    """Test that get_data returns the correct data from a response."""
    expected_data = "test_data"
    with patch.object(Response, "json", return_value={"data": expected_data}):
        response = Response(status_code=200)

    data = get_data(response)

    assert data == expected_data


def test_get_data_missing_key() -> None:
    """
    Test that get_data raises a KeyError when the response
    is missing the 'data' key.
    """
    with patch.object(Response, "json", return_value={"not_data": "test_data"}):
        response = Response(status_code=200)

    with pytest.raises(KeyError):
        get_data(response)


def test_get_data_invalid_json() -> None:
    """Test that get_data raises a ValueError when the response is not valid json."""
    with patch.object(Response, "json", side_effect=ValueError):
        response = Response(status_code=200)

    with pytest.raises(ValueError):
        get_data(response)
