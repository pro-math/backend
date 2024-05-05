from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.cruds import user_crud
from app.dependencies.user_dependencies import user_by_id
from app.models import db_helper
from app.schemas import User, UserCreate, UserUpdate, UserUpdatePartial

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> User:
    return await user_crud.create_user(session=session, user_in=user_in)


@users_router.get("/")
async def get_users(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> list[User]:
    return await user_crud.get_users(session=session)


@users_router.get("/{user_id}/")
async def get_user(
    user: User = Depends(user_by_id),
) -> User:
    return user


@users_router.delete(
    "/{user_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user: User = Depends(user_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await user_crud.delete_user(
        session=session,
        user=user,
    )


@users_router.put("/{user_id}/")
async def update_user(
    user_update: UserUpdate,
    user: User = Depends(user_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> User:
    return await user_crud.update_user(
        session=session,
        user=user,
        user_update=user_update,
    )


@users_router.patch("/{user_id}/")
async def update_user_partial(
    user_update: UserUpdatePartial,
    user: User = Depends(user_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> User:
    return await user_crud.update_user(
        session=session,
        user=user,
        user_update=user_update,
        partial=True,
    )
