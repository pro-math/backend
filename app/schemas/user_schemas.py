from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    is_active: bool = True
    is_superuser: bool = False
    hashed_password: str


class UserUpdate(UserCreate): ...


class UserUpdatePartial(UserCreate):
    is_active: bool | None = None
    username: str | None = None


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class Token(BaseModel):
    access_token: str
    token_type: str
