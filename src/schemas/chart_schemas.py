from pydantic import BaseModel


class Chart(BaseModel):
    date: str
    stats: float
