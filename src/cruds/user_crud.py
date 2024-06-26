from fastapi import status, HTTPException

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User, Achievement
from src.schemas.user_schemas import UserCreate, UserUpdate, UserUpdatePartial
from src.utils.populate_achievements import populate_achievements


async def get_users(session: AsyncSession) -> list[User]:
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(User, user_id)


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    result = await session.execute(select(User).where(User.username == username))
    return result.unique().scalars().one_or_none()


async def create_user(session: AsyncSession, user_in: UserCreate) -> User:
    achievements = await session.execute(select(Achievement))
    if not achievements.unique().scalars().all():
        await populate_achievements(session=session)

    user = User(**user_in.model_dump())
    user_in_db = await get_user_by_username(session=session, username=user.username)
    if user_in_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User {user.username} already exists!",
        )

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def update_user(
    session: AsyncSession,
    user: User,
    user_update: UserUpdate | UserUpdatePartial,
    partial: bool = False,
) -> User:
    for name, value in user_update.model_dump(exclude_unset=partial).items():
        setattr(user, name, value)
    await session.commit()
    return user


async def delete_user(
    session: AsyncSession,
    user: User,
) -> None:
    await session.delete(user)
    await session.commit()
