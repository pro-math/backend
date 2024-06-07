from sqlalchemy import select

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.orm import joinedload
from starlette.exceptions import HTTPException

from src.models import db_helper, Rating as RatingModel, GameSession as GameSessionModel
from src.schemas import GameMode, Rating, OperationType
from src.utils.auth import oauth2_scheme, verify_jwt_token

ratings_router = APIRouter(prefix="/ratings", tags=["Ratings"])


@ratings_router.get("/me/")
async def get_users_ratings(
    game_mode: GameMode,
    examples_category: int,
    math_operations: list[OperationType] = Query(...),
    limit: int = 10,
    offset: int = 0,
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> list[Rating]:
    decoded_data = verify_jwt_token(token)
    if not decoded_data:
        raise HTTPException(status_code=400, detail="Invalid token")
    user_id = decoded_data["sub"]
    query = (
        select(GameSessionModel)
        .options(joinedload(GameSessionModel.user))
        .where(
            GameSessionModel.user_id == user_id,
            GameSessionModel.game_mode == game_mode,
            GameSessionModel.examples_category == examples_category,
            GameSessionModel.math_operations.contains(math_operations),
        )
        .order_by(
            GameSessionModel.duration
            if game_mode == GameMode.count_mode
            else RatingModel.correct_count.desc()
        )
        .limit(limit)
        .offset(offset)
    )

    result = await session.execute(query)
    ratings = result.scalars().all()

    return [
        Rating(
            game_mode=rating.game_mode,
            duration=rating.duration,
            math_operations=rating.math_operations,
            examples_category=rating.examples_category,
            user_id=rating.user_id,
            created_at=rating.created_at,
            game_session_id=rating.id,
        )
        for rating in ratings
    ]


@ratings_router.get("/")
async def get_ratings(
    game_mode: GameMode,
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
        )
        .order_by(
            RatingModel.correct_count / GameSessionModel.total_count
            if game_mode == GameMode.count_mode
            else RatingModel.correct_count.desc(),
            RatingModel.duration.desc()
            if game_mode == GameMode.count_mode
            else RatingModel.correct_count.desc(),
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
