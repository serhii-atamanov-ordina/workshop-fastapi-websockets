from __future__ import annotations

from datetime import datetime
from typing import ClassVar, Optional, Type, Union

from pydantic import BaseModel, Field, field_serializer


def make_all_fields_optional(schema: Type[BaseModel]) -> dict:
    """Makes all fields of a schema optional.

    Args:
        schema: The schema to make all fields optional.

    Returns:
        A schema with all fields optional.

    """
    return {k: Optional[v] for k, v in schema.__annotations__.items()}


class BaseOutputSchema(BaseModel):
    id: Union[str, int] = Field(
        ...,
        title="Id",
        description="The internal primary key.",
    )
    created_at: datetime = Field(
        ...,
        title="Created at",
        description="The time of creation.",
    )

    @field_serializer("id")
    def serialize_id(self, id: str | int) -> str:
        """Serializes all id fields to string."""
        return str(id)


class PostInputSchema(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        examples=["My post label"],
        title="Name",
        description="The name of the post.",
    )
    content: str = Field(
        ...,
        examples=["My content"],
        title="Content",
        description="The content of the post.",
    )
    user_id: int = Field(
        ...,
        examples=[1],
        title="User id",
        description="The owner of the post.",
    )


class PostOutputSchema(BaseOutputSchema, PostInputSchema):
    model_config: ClassVar[dict] = {"from_attributes": True}


class UserInputSchema(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        examples=["My name"],
        title="Name",
        description="The name of the user.",
    )
    password: str = Field(
        ...,
        min_length=1,
        max_length=255,
        examples=["My password"],
        title="Content",
        description="The password of the user.",
    )


class UserOutputSchema(BaseOutputSchema, UserInputSchema):
    model_config: ClassVar[dict] = {"from_attributes": True}
