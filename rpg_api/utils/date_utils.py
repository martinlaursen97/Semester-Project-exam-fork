from datetime import datetime, UTC
from typing import Any
import neo4j.time


def get_datetime_utc() -> datetime:
    """Return current time in UTC."""
    return datetime.now(UTC)


def convert_to_valid_time(input_dict: dict[str, Any]) -> dict[str, Any]:
    "Converts neo time, to valid time input."

    for key, value in input_dict.items():
        if isinstance(value, neo4j.time.DateTime):
            input_dict[key] = datetime(
                value.year,
                value.month,
                value.day,
                value.hour,
                value.minute,
                value.second,
                value.nanosecond // 1000,
            )
    return input_dict
