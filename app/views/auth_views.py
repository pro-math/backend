from fastapi import Depends, APIRouter 
from app.schemas.tokens_schemas import Token
from app.schemas.user_schemas import UserSchema
from utils.auth import encode_jwt

auth_router = APIRouter(prefix="/auth/", tags=["Auth"])

@auth_router.post("/login/")
async def auth_user(
    user: UserSchema = Depends(validate_auth_user)
):
    payload = {
        "sub": user.id,
        "username": user.username,
    }
    token = encode_jwt(payload)
    return Token(
        access_token=token,
        token_type="Bearer",
    )