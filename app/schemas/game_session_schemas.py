import datetime
from enum import Enum
from pydantic import BaseModel, field_validator


class GameMode(str, Enum):
    time_mode = "time"
    count_mode = "count"


class MathOperation(str, Enum):
    plus = "plus"
    minus = "minus"
    multiplication = "multiplication"
    division = "division"


class GameSession(BaseModel):
    game_mode: GameMode
    duration: datetime.timedelta
    math_operations: list[MathOperation]
    examples_category: int
    examples: list[dict[str, str]]
    total_count: int
    correct_count: int
    create_at: datetime.datetime

    @field_validator("examples")
    def check_examples(cls, v):
        for example in v:
            if not {"example_text", "answer_users", "answer_correct"} <= example.keys():
                raise ValueError(
                    "Each example dictionary must contain 'example_text', 'answer_correct' and 'answer_users'"
                )
        return v

    @field_validator("examples_category")
    def check_examples_category(cls, v):
        if v % 10 != 0:
            raise ValueError("examples_category must be divisible by 10")
        return v
