from fastapi import APIRouter

from app.utils.models import User

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.post("/")
async def add_user(user: User) -> User: ...


@users_router.get("/")
async def get_all_users(user: User) -> User: ...


@users_router.get("/{user_id}")
async def get_user_by_user_id(user_id: int) -> User: ...


@users_router.delete("/{user_id}")
async def delete_user_by_user_id(user_id: int) -> dict[str, str]:
    return {"status": "ok"}


@users_router.put("/{user_id}")
async def update_user_by_user_id(user_id: int) -> User: ...


