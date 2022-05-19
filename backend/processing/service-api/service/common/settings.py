import secrets
from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "default_key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1
    ALGORITHM = "HS256"

    CACHE_TTL = 300
    CACHE_MAX_SIZE = 32

    DEFAULT_QUERY_LIMIT = 500

    CORS_ORIGINS: List[str] = ["*"]
    ALLOWED_HOSTS: List[str] = ["*"]

    class Config:
        case_sensitive = True


settings = Settings()
