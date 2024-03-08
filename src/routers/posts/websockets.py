import json

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import WebSocket
from src.core.schemas import PostOutputSchema
from src.routers.posts.controller import get_posts

websocket_connections: set[WebSocket] = set()


async def broadcast_list(session: AsyncSession):
    for connection in websocket_connections:
        pass

        # Only one (probably) broke part of the app, that you should work on.
