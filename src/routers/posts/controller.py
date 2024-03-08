import logging

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import get_settings
from src.core.models import Post
from src.core.schemas import PostInputSchema
from src.database.crud import create, get, delete
from src.routers.users.controller import get_user_by_name

logger = logging.getLogger(get_settings().LOGGER_CONTROLLERS_NAME)


async def create_post(post_input: PostInputSchema, session: AsyncSession, username: str) -> Post:
    """Creates a post."""
    logger.debug("Creating post.")

    user = await get_user_by_name(username, session)

    new_post = await create(
        new_model=Post(**post_input.model_dump()),
        session=session,
    )
    await session.commit()
    return new_post


async def get_posts(session: AsyncSession) -> list[Post]:
    """Returns a list of all posts."""
    logger.debug("Getting all posts.")
    posts = await get(
        Post,
        session,
        [],
    )
    logger.info(f"Found {len(posts)} posts.")
    return posts


async def get_post(post_id: int, session: AsyncSession) -> Post:
    """Returns a post selected by its ID."""
    logger.info(f"Getting post for {post_id}.")

    result = await get(
        Post,
        session,
        [Post.id == post_id],
        expected_count=1,
    )

    return result[0]


async def delete_post(post_id: int, session: AsyncSession) -> None:
    """Deletes a post selected by its ID."""
    await delete(Post, session, [Post.id == post_id])
    await session.commit()

    raise HTTPException(
        status_code=status.HTTP_204_NO_CONTENT,
        detail="The post has been deleted.",
    )
