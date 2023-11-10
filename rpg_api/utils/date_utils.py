from datetime import datetime, UTC


def get_datetime_utc() -> datetime:
    """Return current time in UTC."""
    return datetime.now(UTC)
