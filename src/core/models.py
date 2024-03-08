from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.sql import func

from src.database.database import DeclarativeBase


class BaseModel(DeclarativeBase):
    """Global model inherited by all other models.

    Attributes:
        created_at: The time the model was created.
    """

    __abstract__ = True

    created_at = Column(
        DateTime(),
        default=func.now(),
        nullable=False,
    )


class User(BaseModel):
    """Definition of the user model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)


class Post(BaseModel):
    """Definition of the post model."""

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    content = Column(String(), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
