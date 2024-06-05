from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.cruds import game_session_crud
from app.dependencies.game_session_dependencies import game_session_by_id
from app.models import db_helper
from app.schemas import (
    GameSession,
    GameSessionCreate,
    GameSessionUpdate,
    GameSessionUpdatePartial,
)
from app.views.users_views import oauth2_scheme

game_sessions_router = APIRouter(prefix="/game_sessions", tags=["Game sessions"])


@game_sessions_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create_game_session(
    game_session_in: GameSessionCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    token: str = Depends(oauth2_scheme),
) -> GameSession:
    return await game_session_crud.create_game_session(
        session=session, game_session_in=game_session_in
    )


@game_sessions_router.get("/")
async def get_game_sessions(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> list[GameSession]:
    return await game_session_crud.get_game_sessions(session=session)


@game_sessions_router.get("/{game_session_id}/")
async def get_game_session(
    token: str = Depends(oauth2_scheme),
    game_session: GameSession = Depends(game_session_by_id),
) -> GameSession:
    return game_session


@game_sessions_router.delete(
    "/{game_session_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_game_session(
    game_session: GameSession = Depends(game_session_by_id),
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await game_session_crud.delete_game_session(
        session=session,
        game_session=game_session,
    )


@game_sessions_router.put("/{game_session_id}/")
async def update_game_session(
    game_session_update: GameSessionUpdate,
    game_session: GameSession = Depends(game_session_by_id),
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> GameSession:
    return await game_session_crud.update_game_session(
        session=session,
        game_session=game_session,
        game_session_update=game_session_update,
    )


@game_sessions_router.patch("/{game_session_id}/")
async def update_game_session_partial(
    game_session_update: GameSessionUpdatePartial,
    token: str = Depends(oauth2_scheme),
    game_session: GameSession = Depends(game_session_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> GameSession:
    return await game_session_crud.update_game_session(
        session=session,
        game_session=game_session,
        game_session_update=game_session_update,
        partial=True,
    )
