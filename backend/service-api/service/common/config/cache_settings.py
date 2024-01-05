from pydantic_settings import BaseSettings


class CacheSettings(BaseSettings):
    CACHE_TTL: int = 300
    CACHE_MAX_SIZE: int = 32

    class Config:
        case_sensitive = True


cache_settings = CacheSettings()
