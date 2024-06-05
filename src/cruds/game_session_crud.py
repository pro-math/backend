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


async def get_game_session(
    session: AsyncSession,
    game_session_id: int,
) -> GameSession | None:
    return await session.get(GameSession, game_session_id)


async def create_game_session(
    session: AsyncSession,
    game_session_in: GameSessionCreate,
) -> GameSession:
    game_session = GameSession(**game_session_in.model_dump())
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
