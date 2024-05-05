from sqlalchemy.orm import Mapped

from app.models.base import Base


class User(Base):
    username: Mapped[str]
    email: Mapped[str]
