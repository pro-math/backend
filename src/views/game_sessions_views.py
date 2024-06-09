from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.cruds import game_session_crud, rating_crud
from src.dependencies.game_session_dependencies import game_session_by_id
from src.models import db_helper
from src.schemas import (
    GameSession,
    GameSessionCreate,
)
from src.views.users_views import oauth2_scheme
from src.utils.auth import verify_jwt_token
from src.utils.check_achievements import check_achievements

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
    decoded_data = verify_jwt_token(token)
    if not decoded_data:
        raise HTTPException(status_code=400, detail="Invalid token")
    user_id = decoded_data["sub"]
    game_session = await game_session_crud.create_game_session(
        session=session, user_id=user_id, game_session_in=game_session_in
    )
    await rating_crud.update_rating(
        session=session,
        user_id=user_id,
        game_session=game_session,
    )
    await check_achievements(
        session=session,
        game_session=game_session,
        user_id=user_id,
    )
    return game_session


@game_sessions_router.get("/")
async def get_game_sessions(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> list[GameSession]:
    return await game_session_crud.get_game_sessions(session=session)


@game_sessions_router.get("/me/")
async def get_users_game_sessions(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> list[GameSession]:
    decoded_data = verify_jwt_token(token)
    if not decoded_data:
        raise HTTPException(status_code=400, detail="Invalid token")
    user_id = decoded_data["sub"]
    return await game_session_crud.get_users_game_sessions(
        session=session, user_id=user_id
    )


@game_sessions_router.get("/{game_session_id}/")
async def get_game_session(
    game_session: GameSession = Depends(game_session_by_id),
) -> GameSession:
    return game_session


# @game_sessions_router.delete(
#     "/{game_session_id}/",
#     status_code=status.HTTP_204_NO_CONTENT,
# )
# async def delete_game_session(
#     game_session: GameSession = Depends(game_session_by_id),
#     token: str = Depends(oauth2_scheme),
#     session: AsyncSession = Depends(db_helper.scoped_session_dependency),
# ) -> None:
#     decoded_data = verify_jwt_token(token)
#     if not decoded_data:
#         raise HTTPException(status_code=400, detail="Invalid token")
#     user_id = decoded_data["sub"]
#     await game_session_crud.delete_game_session(
#         session=session,
#         game_session=game_session,
#     )
#

# @game_sessions_router.put("/{game_session_id}/")
# async def update_game_session(
#     game_session_update: GameSessionUpdate,
#     game_session: GameSession = Depends(game_session_by_id),
#     token: str = Depends(oauth2_scheme),
#     session: AsyncSession = Depends(db_helper.scoped_session_dependency),
# ) -> GameSession:
#     updated_game_session = await game_session_crud.update_game_session(
#         session=session,
#         game_session=game_session,
#         game_session_update=game_session_update,
#     )
#     await rating_crud.update_rating(
#         session=session, user_id=game_session.user_id, game_mode=game_session.game_mode
#     )
#     return updated_game_session
#
#
# @game_sessions_router.patch("/{game_session_id}/")
# async def update_game_session_partial(
#     game_session_update: GameSessionUpdatePartial,
#     token: str = Depends(oauth2_scheme),
#     game_session: GameSession = Depends(game_session_by_id),
#     session: AsyncSession = Depends(db_helper.scoped_session_dependency),
# ) -> GameSession:
#     updated_game_session = await game_session_crud.update_game_session(
#         session=session,
#         game_session=game_session,
#         game_session_update=game_session_update,
#         partial=True,
#     )
#     await rating_crud.update_rating(
#         session=session, user_id=game_session.user_id, game_mode=game_session.game_mode
#     )
#     return updated_game_session
