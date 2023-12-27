import pytest
from datetime import datetime, timedelta
from unittest.mock import patch
from rpg_api.web.api.postgres.auth.auth_utils import hash_password, verify_password, _encode_token, create_access_token, create_reset_password_token, decode_token 
from rpg_api.settings import settings
from rpg_api.utils import dtos
import jwt

def test_hash_password():
    """Test hash_password."""

    password = "password"
    hashed_password = hash_password(password)

    assert hashed_password != password
    assert hashed_password is not None

def test_verify_password():
    """Test verify_password."""

    password = "password"
    hashed_password = hash_password(password)

    assert verify_password(password, hashed_password) is True
    assert verify_password("wrong_password", hashed_password) is False