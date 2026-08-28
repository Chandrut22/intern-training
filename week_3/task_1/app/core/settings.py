from typing import Annotated, Any

from pydantic import HttpUrl, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    OPENROUTER_BASE_URL: HttpUrl
    OPENROUTER_API_KEY: str
    MODELS_NAME: Annotated[list[str], NoDecode]  # <- only real change
    TEMPERATURE: float
    MAX_TOKEN: int | None = None

    @field_validator("MODELS_NAME", mode="before")
    @classmethod
    def parse_comma_separated_models(cls, v: Any) -> list[str]:
        if isinstance(v, str):
            v = v.strip("'\" ")
            return [model.strip() for model in v.split(",") if model.strip()]
        return v

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
