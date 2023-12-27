import json
import logging
from typing import Any

from locust import FastHttpUser
from locust.contrib.fasthttp import FastResponse, ResponseContextManager

from uuid import uuid4

PREFIX = "/api/postgres"


def get_user_header(token: str) -> dict[str, Any]:
    """Return access token for given data."""
    return {"Authorization": f"Bearer {token}"}


def get_data(response: ResponseContextManager | FastResponse) -> Any:
    """Return data from a given response."""
    return json.loads(response.content.decode("utf-8"))["data"]


def handle_error(response: ResponseContextManager) -> None:
    """Adds custom error message to be displayed in the web ui and log."""
    error_msg = f"Got unexpected status code {response.status_code}: {response.text}"
    response.failure(error_msg)
    logging.error(error_msg)


def setup_user(user: FastHttpUser) -> tuple[list[str], dict[str, Any]]:
    """
    Set up a user, that will be used for running the tasks.

    Returns id of the test users that were created,
    and the access token header for the user.
    """

    # Create a user on startup that will be used to execute the tasks

    email = f"user{uuid4()}@example.com"
    with user.client.post(
        url=f"{PREFIX}/auth/register",
        json={
            "email": email,
            "password": "password",
        },
        catch_response=True,
    ) as response_test_user:
        if response_test_user.status_code == 201:
            response_test_user_data = get_data(response_test_user)
        else:
            handle_error(response_test_user)
            raise Exception("Create user failed!")

    # Extract id
    id = response_test_user_data

    # Login the user
    with user.client.post(
        url=f"{PREFIX}/auth/login-email",
        json={"email": email, "password": "password"},
        catch_response=True,
    ) as response_login:
        if response_login.status_code == 200:
            token = response_login.json()["data"]["access_token"]
            token_header = get_user_header(token)
        else:
            token_header = {}
            handle_error(response=response_login)
            raise Exception("Login failed!")

    return id, token_header
