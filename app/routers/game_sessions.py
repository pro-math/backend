from fastapi import APIRouter

from app.utils.models import GameSession

game_sessions_router = APIRouter(prefix="/game_sessions", tags=["Game sessions"])


@game_sessions_router.post("/")
async def add_game_session(game_session: GameSession) -> GameSession:
    ...


@game_sessions_router.get("/{game_session_id}")
async def get_game_session_by_game_session_id(game_session_id: int) -> GameSession:
    ...


@game_sessions_router.delete("/{game_session_id}")
async def delete_game_session_by_game_session_id(game_session_id: int) -> GameSession:
    ...


@game_sessions_router.put("/{game_session_id}")
async def update_game_session_by_game_session_id(game_session_id: int) -> GameSession:
    ...

