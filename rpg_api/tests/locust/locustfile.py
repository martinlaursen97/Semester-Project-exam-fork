from locust import FastHttpUser, tag, task
from rpg_api.tests.locust import utils

from uuid import uuid4

PREFIX = "/api/postgres"


class WebUser(FastHttpUser):
    """Default user for load testing."""

    weight = 1

    def on_start(self) -> None:
        """
        Runs before each user is created.

        This will create a user, log the user in and attach data to that user,
        that will later be used e.g. header and id.
        """

        self.user_id, self.token_header = utils.setup_user(self)

    @task
    @tag("alive")
    def test_alive(self) -> None:
        """Test alive."""
        with self.client.get(
            url="/api/monitoring/health",
            headers=self.token_header,
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                utils.handle_error(response)

    @task
    @tag("create_char")
    def create_character(self) -> None:
        """Create character endpoint."""
        with self.client.post(
            url=f"{PREFIX}/characters",
            headers=self.token_header,
            json={
                "base_class_id": "92a85efe-2f9e-4493-8638-5a4396a0f72a",
                "gender": "male",
                "character_name": f"string{uuid4()}",
            },
            catch_response=True,
        ) as response:
            if response.status_code != 201:
                utils.handle_error(response)
