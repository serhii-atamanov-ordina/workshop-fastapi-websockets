"""Centralizes the OpenAPI definitions for the API."""

from enum import Enum


class Descriptions(str, Enum):
    """A class to hold the descriptions of OpenAPI variables.

    This has been centralized to ensure that the descriptions are consistent across the
    API.

    """
    post_id = "Unique id of post"
    user_id = "Unique id of user"


def get_openapi_tags_metadata() -> list[dict[str, str]]:
    """Returns the tag definitions for the swagger documentation.

    Returns:
        The tag definitions.

    """
    return [
        {
            "name": "Posts",
            "description": "Operations to create, read, update or delete posts.",
        },
        {
            "name": "Users",
            "description": "Operations to create, read, update or delete users.",
        },
    ]
