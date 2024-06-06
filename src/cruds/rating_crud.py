from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from src.models import GameSession, Rating
from src.schemas import GameMode


async def get_user_rating(
    session: AsyncSession,
    user_id: int,
    game_mode: str,
    math_operations: list[str],
    examples_category: int,
) -> Rating | None:
    result = await session.execute(
        select(Rating)
        .options(joinedload(Rating.game_session))
        .where(
            Rating.user_id == user_id,
            Rating.game_mode == game_mode,
            Rating.math_operations == math_operations,
            Rating.examples_category == examples_category,
        )
    )
    return result.scalars().first()


async def update_rating(
    session: AsyncSession, user_id: int, game_session: GameSession
) -> None:
    rating = await get_user_rating(
        session,
        user_id=user_id,
        game_mode=game_session.game_mode,
        math_operations=game_session.math_operations,
        examples_category=game_session.examples_category,
    )

    if rating:
        if game_session.game_mode == GameMode.count_mode:
            if game_session.duration < rating.duration:
                rating.duration = game_session.duration
                rating.game_session_id = game_session.id
        elif game_session.game_mode == GameMode.time_mode:
            if game_session.correct_count > rating.game_session.correct_count:
                rating.correct_count = game_session.correct_count
                rating.game_session_id = game_session.id
    else:
        new_rating = Rating(
            game_mode=game_session.game_mode,
            duration=game_session.duration,
            math_operations=game_session.math_operations,
            examples_category=game_session.examples_category,
            game_session_id=game_session.id,
            user_id=user_id,
        )
        session.add(new_rating)

    await session.commit()
