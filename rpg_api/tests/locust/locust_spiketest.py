from locust import FastHttpUser, task, between, events
from locust.runners import MasterRunner, WorkerRunner
import gevent
from typing import Any


class WebUser(FastHttpUser):
    """Default user for load testing."""

    wait_time = between(1, 2)

    @task
    def my_task(self) -> None:
        self.client.get("/api/monitoring/health")


def change_load(
    environment: Any, user_count: int, spawn_rate: int, length_in_seconds: int
) -> None:
    """Change the load during execution of the test."""
    # Change the number of users
    environment.runner.start(user_count, spawn_rate, wait=False)
    gevent.sleep(length_in_seconds)


@events.test_start.add_listener
def on_test_start(environment: Any, **kwargs: dict[Any, Any]) -> None:
    """
    Add eventlistner, this allows us to controle the execution flow of the test,
    allowing us to spike users during the test.
    """
    if isinstance(environment.runner, (MasterRunner, WorkerRunner)):
        return  # Do not execute this on master or worker nodes

    # Schedule the stages of the test

    # Normal load phase 100 users
    gevent.spawn(
        change_load, environment, user_count=100, spawn_rate=10, length_in_seconds=300
    )

    # Spike phase - after 120 seconds we go 1000 users
    gevent.spawn_later(
        300,
        change_load,
        environment,
        user_count=1000,
        spawn_rate=100,
        length_in_seconds=120,
    )

    # Back to normal - after 90 seconds back to 100 users
    gevent.spawn_later(
        420,
        change_load,
        environment,
        user_count=100,
        spawn_rate=10,
        length_in_seconds=300,
    )
    gevent.spawn_later(720, environment.runner.quit)
