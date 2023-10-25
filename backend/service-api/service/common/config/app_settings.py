from typing import List, Any

from pydantic import BaseSettings, Field


class AppSettings(BaseSettings):
    # Mandatory fields
    OPENAI_API_KEY: str
    SPACEPULSE_URL: str
    SPACEPULSE_API_KEY: str
    SPACEPULSE_API_SECRET: str

    # Fields with default values
    DB_HOST: str = "localhost:5432"
    CORE_DB_NAME: str = "orb_core"
    CORE_DB_USER: str = "orbsight"
    CORE_DB_PASSWORD: str = "orbsight"
    DB_ENGINE_NAME: str = "postgresql"

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
    COOKIE_SECURE: bool = True  # set False for local testing
    MAX_WORD_COUNT = 20
    MAXIMUM_KEY_PHRASES = 16

    HOME_URL: str = Field("https://oraika.com")
    WWW_URL: str = Field("https://www.oraika.com")
    ORB_URL: str = Field("https://orb.oraika.com")
    DEMO_URL: str = Field("https://demo.oraika.com")
    CORS_ORIGINS: List[str] = Field([])
    ALLOWED_HOSTS: List[str] = Field(["*"])

    def __init__(self, **values: Any):
        super().__init__(**values)
        origin_urls = [self.HOME_URL, self.WWW_URL, self.ORB_URL, self.DEMO_URL]
        for origin_url in origin_urls:
            if origin_url:
                self.CORS_ORIGINS.append(origin_url)

    class Config:
        case_sensitive = True


app_settings = AppSettings()
