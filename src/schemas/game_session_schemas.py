from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from src.schemas.enums import OperationType
from src.schemas import GameMode


class Example(BaseModel):
    type_operation: OperationType
    number1: int
    number2: int
    correct_answer: int
    user_answer: int


class GameSessionBase(BaseModel):
    game_mode: GameMode
    duration: int
    math_operations: list[OperationType]
    examples_category: int
    examples: list[Example]
    total_count: int
    correct_count: int


class GameSessionCreate(GameSessionBase):
    pass


class GameSessionUpdate(GameSessionBase):
    pass


class GameSessionUpdatePartial(BaseModel):
    game_mode: Optional[GameMode] = None
    duration: Optional[int] = None
    math_operations: Optional[list[OperationType]] = None
    examples_category: Optional[int] = None
    examples: Optional[dict] = None
    total_count: Optional[int] = None
    correct_count: Optional[int] = None


class GameSession(GameSessionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
