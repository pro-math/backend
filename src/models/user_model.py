from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.models.base import Base

if TYPE_CHECKING:
    from src.models import GameSession


class User(Base):
    username: Mapped[str] = mapped_column(unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    hashed_password: Mapped[str]

    game_sessions: Mapped[list["GameSession"]] = relationship(back_populates="user")
