from fastapi import FastAPI

from app.data import settings
from app.routers.game_sessions import game_sessions_router
from app.routers.users import users_router

SECRET_KEY = settings.jwt_settings.secret_key
ALGORITHM = settings.jwt_settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.jwt_settings.access_token_expire_minutes

app = FastAPI()

app.include_router(
    users_router,
)
app.include_router(
    game_sessions_router,
)
