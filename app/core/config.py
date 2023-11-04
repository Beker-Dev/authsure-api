from typing import List, Optional, Type
from pydantic import field_validator, FieldValidationInfo
from pydantic_settings import BaseSettings, DotEnvSettingsSource, PydanticBaseSettingsSource


class Settings(BaseSettings):
    PROJECT_NAME: str
    BACKEND_CORS_ORIGINS: List[str]
    ROOT_PATH: Optional[str] = None

    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URI: Optional[str] = None

    DEFAULT_PAGE_SIZE: Optional[int] = 100

    @field_validator("DATABASE_URI")
    def assemble_db_connection(cls, v: Optional[str], info: FieldValidationInfo) -> str:
        user = info.data.get("POSTGRES_USER")
        password = info.data.get("POSTGRES_PASSWORD")
        server = info.data.get("POSTGRES_SERVER")
        port = info.data.get("POSTGRES_PORT")
        db = info.data.get("POSTGRES_DB")
        return f"postgresql+psycopg2://{user}:{password}@{server}:{port}/{db}"

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (DotEnvSettingsSource(settings_cls=settings_cls, case_sensitive=True, env_file=".env"),)


settings = Settings()
