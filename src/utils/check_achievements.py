from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import GameSession


async def check_achievements(
    session: AsyncSession,
    game_session: GameSession,
    user_id: int,
):
    game_session
