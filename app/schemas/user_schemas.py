import datetime
from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str
    hashed_password: str
    create_at: datetime.datetime
