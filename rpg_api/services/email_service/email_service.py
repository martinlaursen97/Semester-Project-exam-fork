from loguru import logger
from rpg_api.services.email_service.email_interface import (
    AsyncEmailServiceInterface,
    EmailDTO,
)
from sendgrid import SendGridAPIClient, Mail
from rpg_api.settings import settings
import asyncio
from fastapi import Depends


class EmailService(AsyncEmailServiceInterface):
    """Email service."""

    def __init__(
        self,
        sg_client: SendGridAPIClient = Depends(),
    ) -> None:
        self.sg_client = sg_client

    async def send_email(
        self,
        email: EmailDTO,
    ) -> None:
        """Send an email to a given email address."""

        message = Mail(
            from_email=settings.sendgrid_from_email,
            to_emails=email.email,
            subject=email.subject,
            plain_text_content=email.body,
            html_content=email.html,
        )

        async def _send() -> None:
            try:
                response = self.sg_client.send(message)
                if response.status_code < 300:
                    logger.info(f"Email sent to {email.email}")
            except Exception:
                logger.error(f"Error sending email to {email.email}.")

        await asyncio.create_task(_send())


class MockEmailService(AsyncEmailServiceInterface):
    """Mock email service."""

    def __init__(self) -> None:
        self.sent_emails: list[EmailDTO] = []

    async def send_email(
        self,
        email: EmailDTO,
    ) -> None:
        """Send an email to a given email address."""

        self.sent_emails.append(email)
        logger.info(f"Mock email sent to {email.email}")
