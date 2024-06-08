from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import GameMode, Chart
from src.schemas import OperationType
from src.cruds import game_session_crud
from src.models import db_helper
from src.utils.auth import oauth2_scheme, verify_jwt_token

charts_router = APIRouter(prefix="/chart", tags=["Charts"])


@charts_router.get("/me/")
async def get_user_achievements(
    game_mode: GameMode,
    examples_category: int,
    difficulty: int,
    math_operations: list[OperationType] = Query(...),
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> list[Chart]:
    decoded_data = verify_jwt_token(token)
    if not decoded_data:
        raise HTTPException(status_code=400, detail="Invalid token")
    user_id = decoded_data["sub"]

    game_sessions = await game_session_crud.get_users_game_sessions(
        session=session,
        user_id=user_id,
    )

    chart_statistic = []

    for game_session in game_sessions:
        if (
            examples_category == game_session.examples_category
            and math_operations == game_session.math_operations
            and (
                difficulty == game_session.duration
                if game_mode == GameMode.time_mode
                else difficulty == game_session.total_count
            )
        ):
            chart_statistic.append(
                Chart(
                    date=game_session.created_at,
                    stats=game_session.correct_count / game_session.total_count
                    if game_mode == GameMode.count_mode
                    else game_session.correct_count,
                )
            )

    return chart_statistic
