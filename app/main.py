from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.views.game_sessions_views import game_sessions_router
from app.views.users_views import users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(root_path="/api/v1", lifespan=lifespan)

app.include_router(
    users_router,
)
app.include_router(
    game_sessions_router,
)
