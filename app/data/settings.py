import os

from dataclasses import dataclass


@dataclass
class JwtSettings:
    secret_key: str
    algorithm: str
    access_token_expire_minutes: str


@dataclass
class Settings:
    jwt_settings: JwtSettings


def get_settings() -> Settings:
    env = os.environ
    return Settings(
        jwt_settings=JwtSettings(
            secret_key=env.get("SECRET_KEY"),
            algorithm=env.get("ALGORITHM"),
            access_token_expire_minutes=env.get("ACCESS_TOKEN_EXPIRE_MINUTES"),
        )
    )


settings = get_settings()
