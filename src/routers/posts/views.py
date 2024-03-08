"""Contains endpoints for interacting with the posts table."""

from fastapi import APIRouter, Body, Path, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import decode_token
from src.core.openapi import Descriptions
from src.core.schemas import PostOutputSchema, PostInputSchema
from src.database.database import get_database
from src.routers.posts.controller import create_post, get_posts, get_post, delete_post
from src.routers.posts.websockets import broadcast_list

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.post(
    "",
    summary="Create a new post.",
    description="Create a new post.",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Post created."},
        500: {"description": "Connection to the database failed."},

    },
    response_model=PostOutputSchema,
)
async def create(
    post: PostInputSchema = Body(...),
    session: AsyncSession = Depends(get_database),
    username: str = Depends(decode_token),
) -> PostOutputSchema:
    """Creates a post."""

    created_post = await create_post(post_input=post, session=session, username=username)

    await broadcast_list(session)

    return created_post


@router.get(
    "",
    summary="Get all posts.",
    description="Get all posts.",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Posts retrieved."},
        404: {"description": "Too few models found."},
        406: {"description": "Too many models found."},
        500: {"description": "Connection to the database failed."},
    },
    response_model=list[PostOutputSchema,],
)
async def get_all(
        session: AsyncSession = Depends(get_database),
) -> list[PostOutputSchema]:
    """Gets all posts."""
    return await get_posts(session=session)


@router.get(
    "/{post_id}",
    summary="Get a post by its ID.",
    description="This endpoint requires a post ID; it returns the post with that ID.",
    responses={
        200: {"description": "Post with given ID retrieved."},
        404: {"description": "Post not found."},
        406: {"description": "Too many models found."},
        500: {"description": "Connection to the database failed."},
    },
    response_model=PostOutputSchema,
)
async def get_by_id(
        post_id: int = Path(
            ...,
            gt=0,
            description=Descriptions.post_id,
        ),
        session: AsyncSession = Depends(get_database),
) -> PostOutputSchema:
    """Get a post by its ID."""
    return await get_post(post_id, session)


@router.delete(
    "/{post_id}",
    summary="Delete a post by its ID.",
    description="This endpoint requires a post ID; it deletes the post with that ID.",
    responses={
        204: {"description": "Post with the given ID was deleted."},
        404: {"description": "Post not found."},
        406: {"description": "Too many models found."},
        500: {"description": "Connection to the database failed."},
    },
)
async def delete_post_by_id(
    post_id: int = Path(
        ...,
        gt=0,
        description=Descriptions.post_id,
    ),
    session: AsyncSession = Depends(get_database),
    username: str = Depends(decode_token),
) -> None:
    """Delete a post by its ID."""
    await delete_post(post_id, session)

    await broadcast_list(session)
