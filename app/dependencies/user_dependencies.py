from typing import Annotated

from app.models.user_model import User

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

import app.utils.auth

from app.cruds import user_crud
from app.models import db_helper
from app.schemas import User

async def validate_auth_user(
    username: str,
    password: str,
):
    # FIND USER IN DB

    user = User()

    if not auth.validate_password(
        password=password,
        hashed_password=user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid username or password",
        )

    return user

async def user_by_id(
    user_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> User:
    user = await user_crud.get_user(session=session, user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found!",
        )

    return user
