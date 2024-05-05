from pydantic import BaseModel, ConfigDict

from app.schemas import GameMode


class GameSessionBase(BaseModel):
    game_mode: GameMode
    examples_category: int
    total_count: int
    correct_count: int
    user_id: int


class GameSessionCreate(GameSessionBase): ...


class GameSessionUpdate(GameSessionCreate): ...


class GameSessionUpdatePartial(GameSessionCreate):
    game_mode: GameMode | None = None
    examples_category: int | None = None
    total_count: int | None = None
    correct_count: int | None = None
    user_id: int | None = None


class GameSession(GameSessionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
