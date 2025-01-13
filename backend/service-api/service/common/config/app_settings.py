from typing import Any, List

from pydantic import Field
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    APP_NAME: str

    # Mandatory fields
    OPENAI_API_KEY: str = ""
    SPACEPULSE_URL: str = ""
    SPACEPULSE_API_KEY: str = ""
    SPACEPULSE_API_SECRET: str = ""

    # Fields with default values
    DB_HOST: str = "localhost:5432"
    CORE_DB_NAME: str = "orb_core"
    CORE_DB_USER: str = "orbsight"
    CORE_DB_PASSWORD: str = "orbsight"
    DB_ENGINE_NAME: str = "postgresql"

    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "default_key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1
    ALGORITHM: str = "HS256"

    CUBEJS_SECRET_KEY: str = "default_key"
    CUBEJS_API_ENDPOINT: str = "http://localhost:4000/cubejs-api/v1/load"

    SERVICE_PORT: int = 8080

    CACHE_TTL: int = 300
    CACHE_MAX_SIZE: int = 32

    DEFAULT_QUERY_LIMIT: int = 500

    DEFAULT_SESSION_TTL_SECONDS: int = 60 * 60 * 24
    DEFAULT_MAX_CACHE_TTL_SECONDS: int = 60 * 60 * 24 * 30
    COOKIE_SECURE: bool = True  # set False for local testing
    MAX_WORD_COUNT: int = 20
    MAXIMUM_KEY_PHRASES: int = 16

    HOME_URL: str = Field("http://oraika.local:3001")
    WWW_URL: str = Field("http://www.oraika.local:3001")
    ORB_URL: str = Field("http://orb.oraika.local:3002")
    DEMO_URL: str = Field("https://demo.oraika.com")
    CORS_ORIGINS: List[str] = Field([])
    ALLOWED_HOSTS: List[str] = Field(["*"])

    IS_GRAPHQL: bool = False

    def __init__(self, **values: Any):
        super().__init__(**values)
        origin_urls = [self.HOME_URL, self.WWW_URL, self.ORB_URL, self.DEMO_URL]
        for origin_url in origin_urls:
            if origin_url:
                self.CORS_ORIGINS.append(origin_url)

        if not self.DB_HOST.startswith("localhost") and self.APP_NAME == 'prefect-workers':
            envs = [self.OPENAI_API_KEY, self.SPACEPULSE_URL, self.SPACEPULSE_API_KEY, self.SPACEPULSE_API_SECRET]
            for field in envs:
                if not field:
                    raise ValueError(f"{field} is not set")

    class Config:
        case_sensitive = True


app_settings = AppSettings()
