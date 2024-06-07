from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.schemas.enums import OperationType, EnumArray
from src.models.base import Base

if TYPE_CHECKING:
    from src.models import GameSession, User


class Rating(Base):
    game_mode: Mapped[str]
    duration: Mapped[int]
    math_operations: Mapped[list[OperationType]] = mapped_column(
        EnumArray, nullable=False
    )
    examples_category: Mapped[int]
    correct_count: Mapped[int]

    game_session_id: Mapped[int] = mapped_column(
        ForeignKey("game_sessions.id"), nullable=False
    )
    game_session: Mapped["GameSession"] = relationship(
        "GameSession", back_populates="rating", lazy="joined"
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="ratings", lazy="joined")
