from enum import Enum


class GameMode(str, Enum):
    time_mode = "time_mode"
    count_mode = "count_mode"


class OperationType(str, Enum):
    plus = "plus"
    minus = "minus"
    multiplication = "multiplication"
    division = "division"
