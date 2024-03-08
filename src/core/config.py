"""Contains the configurations of the API."""

from __future__ import annotations

import os
from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Defines settings from environment variables and/or dotenv file."""

    model_config = SettingsConfigDict(extra="ignore")

    APP_NAME: str = "Example FastAPI"
    ROOT_PATH: str

    LOG_LEVEL: str
    LOGGING_REQUESTS_FILE: str
    LOGGER_REQUESTS_NAME: str
    LOGGING_CONTROLLERS_FILE: str
    LOGGER_CONTROLLERS_NAME: str

    SERVICE_CONNECTION_TIMEOUT: int = Field(description="s")
    SERVICE_CONNECTION_RETRY_DELAY: int = Field(description="s")


@lru_cache()
def get_settings() -> Settings:
    """Gets cached environment variables as Settings-object."""
    return Settings(_env_file=get_dotenv_file())


def get_environment(
    default: Literal["dev", "test", "prod"] | None = None
) -> Literal["dev", "test", "prod"]:
    """Gets environment as string from environment variable or default if given.

    Raises:
        ValueError if environment is not accepted or ENVIRONMENT variable not set.

    """
    accepted_environments = ["dev", "test", "prod"]

    try:
        environment = os.environ["ENVIRONMENT"]
    except KeyError as e:
        if default is not None:
            environment = default.lower()
        else:
            msg = "ENVIRONMENT is not set"
            raise ValueError(msg) from e

    if environment not in accepted_environments:
        msg = f"environment '{environment}' not accepted"
        raise ValueError(msg)
    return environment  # type: ignore[return-value]


def get_dotenv_file(
    default: Literal["dev", "test", "prod"] = "dev"
) -> Literal[".env.dev", ".env.test", ""]:
    """Gets relevant dotenv-file."""
    environment = get_environment(default=default)

    dotenv_file = f".env.{environment}"
    if environment == "prod":
        dotenv_file = ""
    return dotenv_file  # type: ignore[return-value]
