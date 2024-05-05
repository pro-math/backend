from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Base


class GameSession(Base):
    game_mode: Mapped[str]
    examples_category: Mapped[int]
    total_count_examples: Mapped[int]
    correct_count_examples: Mapped[int]

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
    )
