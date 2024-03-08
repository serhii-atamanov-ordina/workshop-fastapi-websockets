import logging

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import get_settings
from src.core.models import User
from src.core.schemas import UserInputSchema
from src.database.crud import create, get, delete

logger = logging.getLogger(get_settings().LOGGER_CONTROLLERS_NAME)


async def create_user(user_input: UserInputSchema, session: AsyncSession) -> User:
    """Creates a user."""
    logger.debug("Creating user.")
    new_user = await create(
        new_model=User(**user_input.model_dump()),
        session=session,
    )
    await session.commit()
    return new_user


async def get_users(session: AsyncSession) -> list[User]:
    """Returns a list of all users."""
    logger.debug("Getting all users.")
    users = await get(
        User,
        session,
        [],
    )
    logger.info(f"Found {len(users)} users.")
    return users


async def get_user_by_id(user_id: int, session: AsyncSession) -> User:
    """Returns a user selected by its ID."""
    logger.info(f"Getting user for {user_id}.")

    result = await get(
        User,
        session,
        [User.id == user_id],
        expected_count=1,
    )

    return result[0]


async def get_user_by_name(name: str, session: AsyncSession) -> User:
    """Returns a user selected by its ID."""
    logger.info(f"Getting user for {name}.")

    result = await get(
        User,
        session,
        [User.name == name],
        expected_count=1,
    )

    return result[0]


async def delete_user(user_id: int, session: AsyncSession, ) -> None:
    """Deletes a  selected by its ID."""
    await delete(User, session, [User.id == user_id])
    await session.commit()

    raise HTTPException(
        status_code=status.HTTP_204_NO_CONTENT,
        detail="The user has been deleted.",
    )
