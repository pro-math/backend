from datetime import datetime

from pydantic import BaseModel, ConfigDict

from src.schemas.enums import GameMode, OperationType


class RatingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    game_mode: GameMode
    duration: int
    math_operations: list[OperationType]
    examples_category: int
    user_id: int
    game_session_id: int
    created_at: datetime
