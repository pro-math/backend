from typing import TYPE_CHECKING

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from src.models.base import Base

if TYPE_CHECKING:
    from src.models import User

user_achievements_table = Table(
    "user_achievements",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("achievement_id", Integer, ForeignKey("achievements.id")),
)


class Achievement(Base):
    name: Mapped[str]
    description: Mapped[str]
    image: Mapped[str]

    users: Mapped[list["User"]] = relationship(
        secondary=user_achievements_table,
        back_populates="achievements",
        lazy="joined",
    )
