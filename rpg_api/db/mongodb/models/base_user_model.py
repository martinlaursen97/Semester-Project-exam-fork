from datetime import datetime
from beanie import Document


class MBaseUser(Document):
    """BaseUser model for mongodb."""

    first_name: str
    last_name: str
    email: str
    password: str
    created_at: datetime
