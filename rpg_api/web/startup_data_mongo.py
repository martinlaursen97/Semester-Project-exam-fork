from fastapi import FastAPI

from faker import Faker

fake = Faker()


async def create_startup_data_mongo(app: FastAPI) -> None:  # pragma: no cover
    """Create startup classes for the mongodb database."""
