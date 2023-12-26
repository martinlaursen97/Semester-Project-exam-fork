from abc import ABC, abstractmethod
from pydantic import BaseModel


class EmailDTO(BaseModel):
    """Email data transfer object."""

    email: str
    subject: str
    body: str
    html: str | None = None


class AsyncEmailServiceInterface(ABC):
    """Interface for email service."""

    @abstractmethod
    async def send_email(
        self,
        email: EmailDTO,
    ) -> None:
        """Send an email to a given email address."""
        ...
