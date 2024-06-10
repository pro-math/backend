from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.cruds.game_session_crud import (
    get_users_game_sessions,
    get_users_total_correct_count,
)
from src.cruds.achievement_crud import add_achievement_to_user
from src.models import User, Achievement
from src.models.achievement_model import user_achievements_table
from src.schemas import GameSession


async def check_achievements(
    session: AsyncSession,
    game_session: GameSession,
    user_id: int,
):
    user_result = await session.execute(select(User).where(User.id == user_id))
    user = user_result.unique().scalars().one_or_none()

    if not user:
        raise HTTPException(status_code=400, detail="Пользователь не найден")

    user_achievements_result = await session.execute(
        select(Achievement)
        .join(user_achievements_table)
        .where(user_achievements_table.c.user_id == user_id)
    )
    user_achievements = user_achievements_result.unique().scalars().all()

    def has_achievement(achievement_id):
        return any(ach.id == achievement_id for ach in user_achievements)

    new_achievements = []

    if game_session.game_mode == "time_mode":
        if (
            game_session.correct_count >= 10
            and game_session.duration == 15
            and not has_achievement(1)
        ):
            new_achievements.append(1)
        if (
            game_session.correct_count >= 20
            and game_session.duration == 30
            and not has_achievement(2)
        ):
            new_achievements.append(2)
        if (
            game_session.correct_count >= 30
            and game_session.duration == 60
            and not has_achievement(3)
        ):
            new_achievements.append(3)
        if (
            game_session.correct_count >= 40
            and game_session.duration == 90
            and not has_achievement(4)
        ):
            new_achievements.append(4)
        if (
            game_session.correct_count >= 5
            and game_session.duration <= 10
            and not has_achievement(21)
        ):
            new_achievements.append(21)
        if (
            game_session.correct_count >= 50
            and game_session.duration <= 120
            and not has_achievement(26)
        ):
            new_achievements.append(26)
        if (
            game_session.correct_count >= 30
            and game_session.duration <= 45
            and not has_achievement(27)
        ):
            new_achievements.append(27)
        if (
            game_session.correct_count >= 60
            and game_session.duration == 90
            and not has_achievement(39)
        ):
            new_achievements.append(39)
        if (
            game_session.correct_count >= 15
            and game_session.duration == 10
            and not has_achievement(38)
        ):
            new_achievements.append(38)

    elif game_session.game_mode == "count_mode":
        if (
            game_session.correct_count >= 10
            and game_session.total_count == 10
            and not has_achievement(13)
        ):
            new_achievements.append(13)
        if (
            game_session.correct_count >= 12
            and game_session.total_count == 15
            and not has_achievement(14)
        ):
            new_achievements.append(14)
        if (
            game_session.correct_count >= 18
            and game_session.total_count == 20
            and not has_achievement(15)
        ):
            new_achievements.append(15)
        if (
            game_session.correct_count >= 25
            and game_session.total_count == 30
            and not has_achievement(16)
        ):
            new_achievements.append(16)

    if (
        game_session.correct_count >= 10
        and game_session.math_operations == ["+"]
        and not has_achievement(8)
    ):
        new_achievements.append(8)
    if (
        game_session.correct_count >= 10
        and game_session.math_operations == ["-"]
        and not has_achievement(9)
    ):
        new_achievements.append(9)
    if (
        game_session.correct_count >= 10
        and game_session.math_operations == ["*"]
        and not has_achievement(10)
    ):
        new_achievements.append(10)
    if (
        game_session.correct_count >= 10
        and game_session.math_operations == ["/"]
        and not has_achievement(11)
    ):
        new_achievements.append(11)
    if (
        game_session.correct_count >= 10
        and set(game_session.math_operations) == {"+", "-", "*", "/"}
        and not has_achievement(12)
    ):
        new_achievements.append(12)
    if game_session.total_count != 0:
        if (
            game_session.correct_count / game_session.total_count >= 1.0
            and not has_achievement(17)
        ):
            new_achievements.append(17)
        if (
            game_session.correct_count / game_session.total_count >= 0.95
            and game_session.correct_count >= 40
            and not has_achievement(31)
        ):
            new_achievements.append(31)
        if (
            game_session.correct_count / game_session.total_count >= 1.0
            and game_session.total_count == 10
            and not has_achievement(22)
        ):
            new_achievements.append(22)
        if (
            game_session.correct_count / game_session.total_count >= 1.0
            and game_session.total_count >= 50
            and not has_achievement(35)
        ):
            new_achievements.append(35)
        if (
            game_session.correct_count / game_session.total_count >= 1.0
            and game_session.examples_category == 1000
            and not has_achievement(32)
        ):
            new_achievements.append(32)

    if (
        game_session.correct_count >= 10
        and game_session.examples_category == 10
        and game_session.duration <= 15
        and not has_achievement(5)
    ):
        new_achievements.append(5)
    if (
        game_session.correct_count >= 10
        and game_session.examples_category == 100
        and game_session.duration <= 30
        and not has_achievement(6)
    ):
        new_achievements.append(6)
    if (
        game_session.correct_count >= 10
        and game_session.examples_category == 1000
        and game_session.duration <= 60
        and not has_achievement(7)
    ):
        new_achievements.append(7)
    if (
        game_session.correct_count >= 5
        and game_session.examples_category == 1000
        and game_session.duration <= 15
        and not has_achievement(18)
    ):
        new_achievements.append(18)
    if (
        game_session.correct_count >= 20
        and game_session.examples_category == 1000
        and not has_achievement(19)
    ):
        new_achievements.append(19)
    if (
        game_session.correct_count >= 15
        and set(game_session.math_operations) == {"+", "-", "*", "/"}
        and game_session.examples_category == 1000
        and not has_achievement(20)
    ):
        new_achievements.append(20)
    if (
        game_session.correct_count >= 50
        and set(game_session.math_operations) == {"+", "-", "*", "/"}
        and game_session.examples_category == 1000
        and not has_achievement(40)
    ):
        new_achievements.append(40)

    total_correct_count = (
        game_session.correct_count
        + await get_users_total_correct_count(session=session, user_id=user_id)
    )
    if total_correct_count >= 100 and not has_achievement(23):
        new_achievements.append(23)
    if (
        total_correct_count >= 200
        and game_session.math_operations == ["+", "-", "*", "/"]
        and not has_achievement(36)
    ):
        new_achievements.append(36)
    if total_correct_count >= 500 and not has_achievement(29):
        new_achievements.append(29)

    total_sessions_count = len(
        await get_users_game_sessions(session=session, user_id=user_id)
    )
    total_sessions = total_sessions_count + 1
    if total_sessions >= 100 and not has_achievement(28):
        new_achievements.append(28)
    if (
        total_sessions >= 50
        and game_session.correct_count / game_session.total_count >= 0.9
        and not has_achievement(33)
    ):
        new_achievements.append(33)
    if (
        game_session.correct_count / game_session.total_count >= 1.0
        and not has_achievement(30)
    ):
        new_achievements.append(30)

    for achievement_id in new_achievements:
        await add_achievement_to_user(session, user_id, achievement_id)
