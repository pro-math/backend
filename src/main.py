from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.views.game_sessions_views import game_sessions_router
from src.views.users_views import users_router
from src.views.rating_views import ratings_router
from src.views.achievements_view import achievements_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(root_path="/api/v1", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    users_router,
)
app.include_router(
    game_sessions_router,
)
app.include_router(
    ratings_router,
)
app.include_router(
    achievements_router,
)
