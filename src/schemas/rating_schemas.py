from datetime import datetime

from pydantic import BaseModel, ConfigDict

from src.schemas.enums import GameMode, OperationType


class Rating(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    game_mode: GameMode
    duration: int
    math_operations: list[OperationType]
    examples_category: int
    username: str
    total_count: int
    correct_count: int
    user_id: int
    game_session_id: int
    created_at: datetime
