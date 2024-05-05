from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models import GameSession


class User(Base):
    username: Mapped[str]

    game_sessions: Mapped[list["GameSession"]] = relationship(back_populates="user")
