from sqlalchemy import select

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.orm import joinedload
from starlette.exceptions import HTTPException

from src.models import db_helper, Rating as RatingModel, GameSession as GameSessionModel
from src.schemas import GameMode, Rating, OperationType, GameSession
from src.utils.auth import oauth2_scheme, verify_jwt_token

ratings_router = APIRouter(prefix="/ratings", tags=["Ratings"])


@ratings_router.get("/me/")
async def get_users_ratings(
    game_mode: GameMode,
    examples_category: int,
    difficulty: int,
    math_operations: list[OperationType] = Query(...),
    limit: int = 10,
    offset: int = 0,
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> list[GameSession]:
    decoded_data = verify_jwt_token(token)
    if not decoded_data:
        raise HTTPException(status_code=400, detail="Invalid token")
    user_id = decoded_data["sub"]
    query = (
        select(GameSessionModel)
        .where(
            GameSessionModel.user_id == user_id,
            GameSessionModel.game_mode == game_mode,
            GameSessionModel.examples_category == examples_category,
            GameSessionModel.math_operations == math_operations,
            GameSessionModel.duration == difficulty
            if game_mode == GameMode.time_mode
            else GameSessionModel.total_count == difficulty,
        )
        .order_by(
            -GameSessionModel.id,
        )
        .limit(limit)
        .offset(offset)
    )

    result = await session.execute(query)
    ratings = result.scalars().all()

    return [
        GameSession(
            id=rating.id,
            game_mode=rating.game_mode,
            duration=rating.duration,
            math_operations=rating.math_operations,
            examples_category=rating.examples_category,
            examples=rating.examples,
            total_count=rating.total_count,
            correct_count=rating.correct_count,
            created_at=rating.created_at,
        )
        for rating in ratings
    ]


@ratings_router.get("/")
async def get_ratings(
    game_mode: GameMode,
    difficulty: int,
    examples_category: int,
    math_operations: list[OperationType] = Query(...),
    limit: int = 10,
    offset: int = 0,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> list[Rating]:
    query = (
        select(RatingModel)
        .join(RatingModel.game_session)
        .options(joinedload(RatingModel.user))
        .where(
            RatingModel.game_mode == game_mode,
            RatingModel.examples_category == examples_category,
            RatingModel.math_operations == math_operations,
            (
                GameSessionModel.duration == difficulty
                if game_mode == GameMode.time_mode
                else GameSessionModel.total_count == difficulty
            ),
        )
        .order_by(
            -RatingModel.correct_count / GameSessionModel.total_count
            if game_mode == GameMode.count_mode
            else RatingModel.correct_count,
            RatingModel.duration
            if game_mode == GameMode.count_mode
            else RatingModel.correct_count,
        )
        .limit(limit)
        .offset(offset)
    )

    result = await session.execute(query)
    ratings = result.unique().scalars().all()
    return [
        Rating(
            game_mode=rating.game_mode,
            duration=rating.duration,
            math_operations=rating.math_operations,
            examples_category=rating.examples_category,
            user_id=rating.user_id,
            created_at=rating.game_session.created_at,
            game_session_id=rating.game_session_id,
            total_count=rating.game_session.total_count,
            correct_count=rating.game_session.correct_count,
            username=rating.user.username,
        )
        for rating in ratings
    ]
