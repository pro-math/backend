from typing import Annotated

from src.models.user_model import User

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.cruds import user_crud
from src.models import db_helper
from src.schemas import User
from src.utils.auth import oauth2_scheme, verify_jwt_token


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


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> User | None:
    decoded_data = verify_jwt_token(token)
    if not decoded_data:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = await user_crud.get_user(session=session, user_id=decoded_data["sub"])
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    return user
