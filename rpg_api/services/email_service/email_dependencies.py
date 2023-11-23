from sendgrid import SendGridAPIClient
from rpg_api.settings import settings
from rpg_api.services.email_service.email_service import EmailService
from rpg_api.services.email_service.email_service import MockEmailService
from rpg_api.services.email_service.email_interface import AsyncEmailServiceInterface
from typing import Annotated
from fastapi import Depends


def get_email_service() -> AsyncEmailServiceInterface:
    """Get the email service."""
    return EmailService(SendGridAPIClient(settings.sendgrid_api_key))


def get_mock_email_service() -> AsyncEmailServiceInterface:
    """Get the mock email service."""
    return MockEmailService()


GetEmailService = Annotated[
    EmailService,
    Depends(get_email_service),
]
