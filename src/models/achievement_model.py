from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped

from src.models.base import Base

if TYPE_CHECKING:
    pass


class Achievement(Base):
    name: Mapped[str]
    description: Mapped[str]
    image: Mapped[str]
