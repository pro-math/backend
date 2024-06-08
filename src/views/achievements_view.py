from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.cruds import achievement_crud
from src.models import db_helper
from src.schemas import Achievement
from src.utils.auth import oauth2_scheme, verify_jwt_token

achievements_router = APIRouter(prefix="/achievements", tags=["Achievements"])


@achievements_router.get("/")
async def get_all_achievements(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> list[Achievement]:
    return await achievement_crud.get_achievements(session=session)


@achievements_router.get("/me/")
async def get_user_achievements(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> list[Achievement]:
    decoded_data = verify_jwt_token(token)
    if not decoded_data:
        raise HTTPException(status_code=400, detail="Invalid token")
    user_id = decoded_data["sub"]
    return await achievement_crud.get_user_achievements(
        user_id=user_id,
        session=session,
    )
