from typing import List, Any

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "default_key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1
    ALGORITHM = "HS256"

    CUBEJS_SECRET_KEY: str = "default_key"
    CUBEJS_API_ENDPOINT: str = "http://localhost:4000/cubejs-api/v1/load"

    SERVICE_PORT = 8080

    CACHE_TTL = 300
    CACHE_MAX_SIZE = 32

    DEFAULT_QUERY_LIMIT = 500

    DEFAULT_SESSION_TTL_SECONDS = 60 * 60 * 24
    DEFAULT_MAX_CACHE_TTL_SECONDS = 60 * 60 * 24 * 30
    COOKIE_SECURE: bool = True

    ORB_URL: str = Field("https://orb.oraika.com")
    DEMO_URL: str = Field("https://demo.oraika.com")
    CORS_ORIGINS: List[str] = Field([])
    ALLOWED_HOSTS: List[str] = Field(["*"])

    def __init__(self, **values: Any):
        super().__init__(**values)
        self.CORS_ORIGINS.append(self.ORB_URL)
        self.CORS_ORIGINS.append(self.DEMO_URL)

    class Config:
        case_sensitive = True


settings = Settings()
