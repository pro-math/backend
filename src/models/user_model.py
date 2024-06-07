from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.models.base import Base

if TYPE_CHECKING:
    from src.models import GameSession, Rating, Achievement


class User(Base):
    username: Mapped[str] = mapped_column(unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    hashed_password: Mapped[str]

    achievements_ids: Mapped[list[int]] = mapped_column(
        ForeignKey("achievements.id"), nullable=True
    )
    achievements: Mapped[list["Achievement"]] = relationship()
    game_sessions: Mapped[list["GameSession"]] = relationship(back_populates="user")
    ratings: Mapped[list["Rating"]] = relationship(back_populates="user", lazy="joined")
