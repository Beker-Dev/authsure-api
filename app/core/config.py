import secrets
from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str
    BACKEND_CORS_ORIGINS: List[str]
    ROOT_PATH: Optional[str] = None
    DATABASE_URI: str = None

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
