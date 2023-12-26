from typing import Any

from fastapi import HTTPException


class RowNotFoundError(Exception):
    """Exception for when a row is not found in database."""

    def __init__(self, model_name: str | None = None, message: str | None = None):
        if model_name is None:
            message = "Row not found."
        elif message is None:
            message = f"Row not found in {model_name}."
        super().__init__(message)

        self.model_name = model_name


class UniqueConstraintError(Exception):
    """Exception for when a unique constraint is violated."""

    def __init__(self, message: str | None = None, status: int = 409):
        if message is None:
            message = "Unique constraint violated."
        self.message = message
        self.status = status
        super().__init__(message)


class DatabaseError(Exception):
    """Exception for when an unknown database error occurs."""

    def __init__(self, message: str | None = None):
        if message is None:
            message = "Database error."
        super().__init__(message)


class BaseHTTPException(HTTPException):
    """
    Base class for all HTTP exceptions.
    - `message` is the message to be displayed to the user.
    - `dev_message` is the message to be displayed to the developer.
    - `detail` is extra data sent to the client device.
    """

    def __init__(  # noqa: WPS211 (too many arguments)
        self,
        status_code: int,
        message: str | None = None,
        dev_message: str | None = None,
        detail: Any = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code, message, headers)
        self.dev_message = dev_message
        self.data = detail


class HttpBadRequest(BaseHTTPException):
    """400 Bad Request."""

    def __init__(self, message: str = "Bad Request.", **kwargs: Any) -> None:
        super().__init__(400, message, **kwargs)


class HttpUnauthorized(BaseHTTPException):
    """401 Unauthorized."""

    def __init__(self, message: str = "Unauthorized.", **kwargs: Any) -> None:
        super().__init__(401, message, **kwargs)


class HttpForbidden(BaseHTTPException):
    """403 Forbidden."""

    def __init__(self, message: str = "Forbidden.", **kwargs: Any) -> None:
        super().__init__(403, message, **kwargs)


class HttpNotFound(BaseHTTPException):
    """404 Not Found."""

    def __init__(self, message: str = "Not Found.", **kwargs: Any) -> None:
        super().__init__(404, message, **kwargs)


class HttpConflict(BaseHTTPException):
    """409 Conflict."""

    def __init__(self, message: str = "Conflict.", **kwargs: Any) -> None:
        super().__init__(409, message, **kwargs)


class HttpGone(BaseHTTPException):
    """410 Gone."""

    def __init__(self, message: str = "Gone.", **kwargs: Any) -> None:
        super().__init__(410, message, **kwargs)


class HttpTooManyRequests(BaseHTTPException):
    """429 Too Many Requests."""

    def __init__(self, message: str = "Too Many Requests.", **kwargs: Any) -> None:
        super().__init__(429, message, **kwargs)


class HttpUnprocessableEntity(BaseHTTPException):
    """422 Unprocessable Entity."""

    def __init__(self, message: str = "Unprocessable Entity.", **kwargs: Any) -> None:
        super().__init__(422, message, **kwargs)


class HttpInternalServerError(BaseHTTPException):
    """500 Internal Server Error."""

    def __init__(self, message: str = "Internal Server Error.", **kwargs: Any) -> None:
        super().__init__(500, message, **kwargs)
