from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import GameSession
from src.schemas import GameSessionCreate, GameSessionUpdate, GameSessionUpdatePartial


async def get_game_sessions(session: AsyncSession) -> list[GameSession]:
    stmt = select(GameSession).order_by(GameSession.id)
    result: Result = await session.execute(stmt)
    game_sessions = result.scalars().all()
    return list(game_sessions)


async def get_users_game_sessions(
    session: AsyncSession, user_id: int
) -> list[GameSession]:
    stmt = (
        select(GameSession)
        .order_by(GameSession.id)
        .where(GameSession.user_id == user_id)
    )
    result: Result = await session.execute(stmt)
    game_sessions = result.scalars().all()
    return list(game_sessions)


# /api/v1/ratings/?game_mode=count_mode&examples_category=10&math_operations=%2B&math_operations=%2F&math_operations=-&math_operations=*
# /api/v1/ratings/?game_mode=count_mode&examples_category=10&math_operations=%2B&math_operations=-&math_operations=%2A&math_operations=%2F


async def get_users_total_correct_count(session: AsyncSession, user_id: int) -> int:
    game_sessions = await get_users_game_sessions(session=session, user_id=user_id)
    total_correct_count = 0
    for game_session in game_sessions:
        total_correct_count += game_session.correct_count
    return total_correct_count


async def get_game_session(
    session: AsyncSession,
    game_session_id: int,
) -> GameSession | None:
    return await session.get(GameSession, game_session_id)


async def create_game_session(
    session: AsyncSession,
    user_id: int,
    game_session_in: GameSessionCreate,
) -> GameSession:
    game_session = GameSession(
        **game_session_in.model_dump(),
        user_id=user_id,
    )
    session.add(game_session)
    await session.commit()
    await session.refresh(game_session)
    return game_session


async def update_game_session(
    session: AsyncSession,
    game_session: GameSession,
    game_session_update: GameSessionUpdate | GameSessionUpdatePartial,
    partial: bool = False,
) -> GameSession:
    for name, value in game_session_update.model_dump(exclude_unset=partial).items():
        setattr(game_session, name, value)
    await session.commit()
    return game_session


async def delete_game_session(
    session: AsyncSession,
    game_session: GameSession,
) -> None:
    await session.delete(game_session)
    await session.commit()
