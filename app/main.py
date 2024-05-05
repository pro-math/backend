from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.models import db_helper, Base
from app.views.game_sessions_views import game_sessions_router
from app.views.users_views import users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(
    users_router,
)
app.include_router(
    game_sessions_router,
)
