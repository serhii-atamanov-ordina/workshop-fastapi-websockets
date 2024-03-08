import tracemalloc

import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi import WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import get_settings
from src.core.loggers import setup_logging
from src.core.openapi import get_openapi_tags_metadata
from src.database.database import engine, DeclarativeBase
from src.database.database import get_database
from src.routers.posts import views as posts_views
from src.routers.posts.websockets import broadcast_list, websocket_connections
from src.routers.users import views as users_views

tracemalloc.start()

views = [
    posts_views,
    users_views,
]

ROOT_PATH = get_settings().ROOT_PATH

# Set up the loggers.
logger_settings = {
    "LOG_LEVEL": get_settings().LOG_LEVEL,
    "LOGGING_REQUESTS_FILE": get_settings().LOGGING_REQUESTS_FILE,
    "LOGGER_REQUESTS_NAME": get_settings().LOGGER_REQUESTS_NAME,
    "LOGGING_CONTROLLERS_FILE": get_settings().LOGGING_CONTROLLERS_FILE,
    "LOGGER_CONTROLLERS_NAME": get_settings().LOGGER_CONTROLLERS_NAME,
}
setup_logging(logger_settings=logger_settings)

tag_metadata = get_openapi_tags_metadata()
app = FastAPI(
    title="Example FastAPI",
    version="0.0.1",
    swagger_ui_parameters={"operationsSorter": "method"},
    openapi_tags=tag_metadata,
    redoc_url=f"{ROOT_PATH}/redoc",
    docs_url=f"{ROOT_PATH}/docs",
    openapi_url=f"{ROOT_PATH}/openapi.json",
    debug=True,
)
prefix_router = APIRouter(prefix=ROOT_PATH)
for view in views:
    prefix_router.include_router(view.router)
app.include_router(prefix_router)

# CORS middleware.
origins: list[str] = []
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Set up the database
@app.on_event("startup")
async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(DeclarativeBase.metadata.drop_all)
        await conn.run_sync(DeclarativeBase.metadata.create_all)


@app.websocket("/ws")
async def websocket_endpoint_main(websocket: WebSocket, session: AsyncSession = Depends(get_database)):
    await websocket.accept()
    websocket_connections.add(websocket)

    try:
        while True:
            try:
                data = await websocket.receive_text()
                await broadcast_list(session)
            except WebSocketDisconnect:
                break
    finally:
        websocket_connections.remove(websocket)

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)
