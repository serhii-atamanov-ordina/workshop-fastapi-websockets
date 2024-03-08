"""Contains endpoints for interacting with the users table."""
from typing import Optional

from fastapi import APIRouter, Body, Path, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import decode_token
from src.core.openapi import Descriptions
from src.core.schemas import UserOutputSchema, UserInputSchema
from src.database.database import get_database
from src.routers.users.controller import create_user, get_users, get_user_by_id, delete_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "",
    summary="Create a new user.",
    description="Create a new user.",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "User created."},
        500: {"description": "Connection to the database failed."},

    },
    response_model=UserOutputSchema,
)
async def create(
    user: UserInputSchema = Body(...),
    session: AsyncSession = Depends(get_database),
    # name: str = Depends(decode_token),
    # websocket: Optional[WebSocket] = None,
) -> UserOutputSchema:
    """Creates a user."""

    return await create_user(user_input=user, session=session)


@router.get(
    "",
    summary="Get all users.",
    description="Get all users.",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Users retrieved."},
        404: {"description": "Too few models found."},
        406: {"description": "Too many models found."},
        500: {"description": "Connection to the database failed."},
    },
    response_model=list[UserOutputSchema,],
)
async def get_all(
    session: AsyncSession = Depends(get_database),
) -> list[UserOutputSchema]:
    """Gets all users."""
    return await get_users(session=session)


@router.get(
    "/{user_id}",
    summary="Get a user by its ID.",
    description="This endpoint requires a user ID; it returns the user with that ID.",
    responses={
        200: {"description": "User with given ID retrieved."},
        404: {"description": "User not found."},
        406: {"description": "Too many models found."},
        500: {"description": "Connection to the database failed."},
    },
    response_model=UserOutputSchema,
)
async def get_by_id(
    user_id: int = Path(
        ...,
        gt=0,
        description=Descriptions.user_id,
    ),
    session: AsyncSession = Depends(get_database),
) -> UserOutputSchema:
    """Get a user by its ID."""
    return await get_user_by_id(user_id, session)


@router.delete(
    "/{user_id}",
    summary="Delete a user by its ID.",
    description="This endpoint requires a user ID; it deletes the user with that ID.",
    responses={
        204: {"description": "User with the given ID was deleted."},
        404: {"description": "User not found."},
        406: {"description": "Too many models found."},
        500: {"description": "Connection to the database failed."},
    },
)
async def delete_user_by_id(
    user_id: int = Path(
        ...,
        gt=0,
        description=Descriptions.user_id,
    ),
    session: AsyncSession = Depends(get_database),
    username: str = Depends(decode_token),
) -> None:
    """Delete a user by its ID."""
    await delete_user(user_id, session)
