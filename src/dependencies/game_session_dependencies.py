from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.cruds import game_session_crud
from src.models import db_helper
from src.schemas import GameSession


async def game_session_by_id(
    game_session_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> GameSession:
    game_session = await game_session_crud.get_game_session(
        session=session,
        game_session_id=game_session_id,
    )
    if game_session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game session {game_session_id} not found!",
        )

    return game_session
