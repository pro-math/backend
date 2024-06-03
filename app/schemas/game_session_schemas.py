from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas import GameMode


class GameSessionBase(BaseModel):
    game_mode: GameMode
    duration: datetime
    math_operations: list[str]
    examples_category: int
    examples: dict
    total_count: int
    correct_count: int
    user_id: int


class GameSessionCreate(GameSessionBase):
    pass


class GameSessionUpdate(GameSessionBase):
    pass


class GameSessionUpdatePartial(BaseModel):
    game_mode: Optional[GameMode] = None
    duration: Optional[datetime] = None
    math_operations: Optional[list[str]] = None
    examples_category: Optional[int] = None
    examples: Optional[dict] = None
    total_count: Optional[int] = None
    correct_count: Optional[int] = None
    user_id: Optional[int] = None


class GameSession(GameSessionBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
