from enum import Enum

from sqlalchemy import TypeDecorator, ARRAY, String


class GameMode(str, Enum):
    time_mode = "time_mode"
    count_mode = "count_mode"


class OperationType(str, Enum):
    plus = "+"
    minus = "-"
    multiplication = "*"
    division = "/"


class EnumArray(TypeDecorator):
    impl = ARRAY(String)

    def process_bind_param(self, value, dialect):
        if value:
            return [v.value for v in value]
        return value

    def process_result_value(self, value, dialect):
        if value:
            return [OperationType(v) for v in value]
        return value
