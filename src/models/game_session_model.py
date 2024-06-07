from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.schemas.enums import OperationType, EnumArray
from src.models import Base

if TYPE_CHECKING:
    from src.models import User, Rating


class GameSession(Base):
    __tablename__ = "game_sessions"

    game_mode: Mapped[str]
    duration: Mapped[int]
    math_operations: Mapped[list[OperationType]] = mapped_column(
        EnumArray, nullable=False
    )
    examples_category: Mapped[int]
    examples: Mapped[dict] = mapped_column(JSON, nullable=False)
    total_count: Mapped[int]
    correct_count: Mapped[int]
    created_at = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="game_sessions")

    rating: Mapped["Rating"] = relationship(back_populates="game_session")
