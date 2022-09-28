from typing import List

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "default_key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1
    ALGORITHM = "HS256"

    CUBEJS_SECRET_KEY: str = "default_key"
    CUBEJS_API_ENDPOINT: str = "http://localhost:4000/cubejs-api/v1/load"

    CACHE_TTL = 300
    CACHE_MAX_SIZE = 32

    DEFAULT_QUERY_LIMIT = 500

    CORS_ORIGINS: List[str] = Field(["*"])
    ALLOWED_HOSTS: List[str] = Field(["*"])

    class Config:
        case_sensitive = True


settings = Settings()
