from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase): ...


class UserUpdate(UserCreate): ...


class UserUpdatePartial(UserCreate):
    username: str | None = None
    email: str | None = None


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
