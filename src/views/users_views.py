from fastapi import APIRouter, Depends, status, HTTPException
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.cruds import user_crud
from src.dependencies.user_dependencies import user_by_id, get_current_user
from src.models import db_helper
from src.schemas import User, UserCreate, UserUpdate, UserUpdatePartial
from src.schemas.user_schemas import Token, AuthenticationData
from src.utils.auth import create_jwt_token, oauth2_scheme, verify_jwt_token

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get("/me/")
async def get_user_me(current_user: User = Depends(get_current_user)) -> User:
    return current_user


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
    "/me/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    decoded_data = verify_jwt_token(token)
    if not decoded_data:
        raise HTTPException(status_code=400, detail="Invalid token")
    user_id = decoded_data["sub"]
    user = await user_crud.get_user(session=session, user_id=user_id)
    await user_crud.delete_user(
        session=session,
        user=user,
    )


@users_router.put("/{user_id}/")
async def update_user(
    user_update: UserUpdate,
    token: str = Depends(oauth2_scheme),
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
    token: str = Depends(oauth2_scheme),
    user: User = Depends(user_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> User:
    return await user_crud.update_user(
        session=session,
        user=user,
        user_update=user_update,
        partial=True,
    )


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@users_router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    authentication_data: AuthenticationData,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> dict[str, str]:
    username = authentication_data.username
    password = authentication_data.password
    hashed_password = pwd_context.hash(password)
    user_in = UserCreate(
        username=username,
        hashed_password=hashed_password,
        is_superuser=False,
        is_active=True,
    )
    await user_crud.create_user(session=session, user_in=user_in)
    return {"status": "ok"}


@users_router.post("/token")
async def authenticate_user(
    authentication_data: AuthenticationData,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Token:
    username = authentication_data.username
    password = authentication_data.password
    user = await user_crud.get_user_by_username(session=session, username=username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    is_password_correct = pwd_context.verify(password, user.hashed_password)

    if not is_password_correct:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    jwt_token = create_jwt_token({"sub": user.id})
    return Token(access_token=jwt_token, token_type="bearer")
