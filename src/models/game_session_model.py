from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, DateTime, JSON, Integer, ARRAY, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base

if TYPE_CHECKING:
    from src.models import User


class GameSession(Base):
    __tablename__ = "game_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    game_mode: Mapped[str] = mapped_column(String, nullable=False)
    duration: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    math_operations: Mapped[list] = mapped_column(ARRAY(String), nullable=False)
    examples_category: Mapped[int] = mapped_column(Integer, nullable=False)
    examples: Mapped[dict] = mapped_column(JSON, nullable=False)
    total_count: Mapped[int] = mapped_column(Integer, nullable=False)
    correct_count: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="game_sessions")
