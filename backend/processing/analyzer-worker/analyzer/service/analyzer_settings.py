from pydantic import BaseSettings


class AnalyzerSettings(BaseSettings):
    CACHE_TTL = 300
    CACHE_MAX_SIZE = 32

    class Config:
        case_sensitive = True


analyzer_settings = AnalyzerSettings()
