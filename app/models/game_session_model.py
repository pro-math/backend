from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base

if TYPE_CHECKING:
    from app.models import User


class GameSession(Base):
    __tablename__ = "game_sessions"

    game_mode: Mapped[str]
    examples_category: Mapped[int]
    total_count_examples: Mapped[int]
    correct_count_examples: Mapped[int]

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
    )
    user: Mapped["User"] = relationship(back_populates="game_sessions")
