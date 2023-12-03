import enum
from pathlib import Path
from tempfile import gettempdir

from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL
from pydantic import SecretStr

TEMP_DIR = Path(gettempdir())


class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    host: str = "127.0.0.1"
    port: int = 7070
    # quantity of workers for uvicorn
    workers_count: int = 1
    # Enable uvicorn reloading
    reload: bool = False

    # Current environment
    environment: str = "dev"

    log_level: LogLevel = LogLevel.INFO
    # Variables for the database
    db_host: str = "localhost"
    db_port: int = 5435
    db_user: str = "rpg_api"
    db_pass: str = "rpg_api"
    db_base: str = "rpg_api"
    db_echo: bool = False

    # Variables for the JWT
    secret_key: SecretStr = SecretStr("secret")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 600
    reset_password_token_expire_minutes: int = 30

    # Variables for the mongodb
    mongo_host: str = "localhost"
    mongo_port: int = 27017
    mongo_user: str = "rpg_api"
    mongo_pass: str = "rpg_api"
    mongo_database: str = "rpg_api"

    # Sendgrid
    sendgrid_api_key: str = "SG"
    sendgrid_from_email: str = "martin_laursen9@hotmail.com"

    # Frontend
    frontend_url: str = "http://localhost:3000"

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """

        return URL.build(
            scheme="postgresql+asyncpg",
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_pass,
            path=f"/{self.db_base}",
        )

    @property
    def mongodb_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="mongodb",
            host=self.mongo_host,
            port=self.mongo_port,
            user=self.mongo_user,
            password=self.mongo_pass,
            path=f"/{self.mongo_database}",
            query={"authSource": "admin"},
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="RPG_API_",
        env_file_encoding="utf-8",
    )


settings = Settings()
