"""Centralized logging for the application."""

from logging import Formatter, getLogger, FileHandler


def setup_logging(logger_settings: dict[str, str]) -> None:
    """A function to set up the logging. This is centralized to ensure that the logging
    is easily swappable and consistent across the application.

    Args:
        logger_settings: A dictionary containing the logger settings.

    """
    formatter = Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    loggers = [
        (
            logger_settings["LOGGING_REQUESTS_FILE"],
            logger_settings["LOGGER_REQUESTS_NAME"],
        ),
        (
            logger_settings["LOGGING_CONTROLLERS_FILE"],
            logger_settings["LOGGER_CONTROLLERS_NAME"],
        ),
    ]
    for filename, logger_name in loggers:
        logger = getLogger(logger_name)
        logger.setLevel(logger_settings["LOG_LEVEL"])
        handler = FileHandler(filename)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
