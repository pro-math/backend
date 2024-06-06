from sqlalchemy import select

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.orm import joinedload
from starlette.exceptions import HTTPException

from src.models import db_helper, Rating as RatingModel, GameSession as GameSessionModel
from src.schemas import GameMode, RatingResponse, OperationType
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
) -> list[RatingResponse]:
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
        RatingResponse(
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
) -> list[RatingResponse]:
    query = (
        select(RatingModel)
        .options(joinedload(RatingModel.user))
        .where(
            RatingModel.game_mode == game_mode,
            RatingModel.examples_category == examples_category,
            RatingModel.math_operations.contains(math_operations),
        )
        .order_by(
            RatingModel.duration
            if game_mode == GameMode.count_mode
            else RatingModel.correct_count.desc()
        )
        .limit(limit)
        .offset(offset)
    )

    # Execute the query and fetch results
    result = await session.execute(query)
    ratings = result.scalars().all()

    return [
        RatingResponse(
            game_mode=rating.game_mode,
            duration=rating.duration,
            math_operations=rating.math_operations,
            examples_category=rating.examples_category,
            user_id=rating.user_id,
            created_at=rating.game_session.created_at,
            game_session_id=rating.game_session_id,
        )
        for rating in ratings
    ]
