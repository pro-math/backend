import jwt
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer

from app.data import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


def create_jwt_token(data: dict):
    expiration = datetime.utcnow() + timedelta(settings.expiration_time_in_minutes)
    data.update({"exp": expiration})
    token = jwt.encode(data, settings.secret_key, algorithm=settings.algorithm)
    return token


def verify_jwt_token(token: str) -> dict:
    try:
        decoded_data = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        print(decoded_data)
        return decoded_data
    except jwt.PyJWTError:
        return None
