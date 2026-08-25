from typing import Annotated, Any

from pydantic import field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

from app.utils.parse import parse_comma_separated_list


class Settings(BaseSettings):
    OPENROUTER_BASE_URL: str
    OPENROUTER_API_KEY: str
    MODELS_NAME: Annotated[list[str], NoDecode]
    TEMPERATURE: float = 0.7
    MAX_TOKEN: int | None = None
    DATABASE_URL: str
    DEBUG: bool = False

    @field_validator("MODELS_NAME", mode="before")
    @classmethod
    def _parse_models(cls, v: Any) -> list[str]:
        return parse_comma_separated_list(v)

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
