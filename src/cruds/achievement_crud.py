from fastapi import HTTPException
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User
from src.cruds import user_crud
from src.models import Achievement


async def get_achievements(session: AsyncSession) -> list[Achievement]:
    stmt = select(Achievement).order_by(Achievement.id)
    result: Result = await session.execute(stmt)
    achievements = result.scalars().unique().all()
    return list(achievements)


async def get_user_achievements(
    user_id: int,
    session: AsyncSession,
) -> list[Achievement]:
    user = await user_crud.get_user(session=session, user_id=user_id)
    achievements = []
    if user:
        achievements = user.achievements
    return list(achievements) if achievements else []


async def add_achievement_to_user(
    session: AsyncSession,
    user_id: int,
    achievement_id: int,
) -> None:
    user_result = await session.execute(select(User).where(User.id == user_id))
    user = user_result.unique().scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    achievement_result = await session.execute(
        select(Achievement).where(Achievement.id == achievement_id)
    )
    achievement = achievement_result.unique().scalar_one_or_none()

    if not achievement:
        raise HTTPException(status_code=400, detail="Achievement not found")

    if achievement not in user.achievements:
        user.achievements.append(achievement)
        await session.commit()
