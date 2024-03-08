"""CRUD operations."""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Callable, Iterable, Type

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy.sql.operators import ColumnOperators

from src.core.config import get_settings
from src.core.models import BaseModel

logger = logging.getLogger(get_settings().LOGGER_CONTROLLERS_NAME)


def _retry_sql_alchemy_error(
    function: Callable,
) -> Callable:
    """Decorator to retry a function if it raises a SQLAlchemy error.

    Args:
        function: The function to retry.

    Returns:
        The return value of the function.

    Notes:
        There seems to be an occasional SQLAlchemy error when calling the
        database after a long period of inactivity on police infrastructure.
        This decorator will retry the function if it raises an SQLAlchemy error.

    """

    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return await function(*args, **kwargs)
        except SQLAlchemyError as error:
            logger.error(f"SQLAlchemy error: {error}.")
            await asyncio.sleep(0.5)
            return await function(*args, **kwargs)

    return wrapper


@_retry_sql_alchemy_error
async def get(
    model: type[BaseModel],
    session: AsyncSession,
    query: Iterable[
        Type[BinaryExpression] | Type[ColumnOperators]
    ],
    expected_count: int | None = None,
) -> list[BaseModel]:
    """Get a model if it exists.

    Args:
        model: The model class.
        session: The database session.
        query: The arguments to filter by.
        expected_count: The expected number of results. If None, any number of results
                        is allowed.

    Returns:
        List of instances of the queried model.

    Raises:
        404: If too few models are found.
        406: If too many models are found.
        500: If the connection to the database fails.

    """
    logger.debug(f"Querying for {model.__name__}.")

    results = await session.execute(model.__table__.select().where(*query))
    results = results.all()

    if expected_count is None or len(results) == expected_count:
        return results

    logger.error(f"Expected {expected_count} {model.__name__} but found {len(results)}.")
    if len(results) < expected_count:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not enough models match the query.",
        )
    raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail="Too many models match the query.",
    )


@_retry_sql_alchemy_error
async def create(new_model: BaseModel, session: AsyncSession) -> BaseModel:
    """Create a model.

    Args:
        new_model: The model to create.
        session: The database session.

    Returns:
        Instance of the created model.

    Raises:
        500 If the connection to the database fails.

    """
    logger.info(f"Creating {new_model.__class__.__name__}.")
    session.add(new_model)
    await session.flush()
    await session.refresh(new_model)

    return new_model


@_retry_sql_alchemy_error
async def delete(
    model: type[BaseModel],
    session: AsyncSession,
    query: Iterable[BinaryExpression],
) -> str:
    """Delete a model.

    Args:
        model: The model class.
        session: The database session.
        query: The arguments to filter by.

    Returns:
        "ok" if the model was deleted.

    Raises:
        HTTPException: 500 If the connection to the database fails.

    """
    logger.info(f"Deleting model: {model.__name__}.")
    await get(model, session, query, expected_count=1)
    await session.execute(model.__table__.delete().where(*query))

    return "ok"
