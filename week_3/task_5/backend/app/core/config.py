from contextvars import ContextVar
from typing import Annotated, Any

from pydantic import field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

from app.utils.parse import parse_comma_separated_list

request_id_ctx: ContextVar[str] = ContextVar(
    "request_id",
    default="-",
)


class Settings(BaseSettings):
    OPENROUTER_BASE_URL: str
    OPENROUTER_API_KEY: str
    MODELS_NAME: Annotated[list[str], NoDecode]
    TEMPERATURE: float = 0.7
    MAX_TOKEN: int | None = None
    DATABASE_URL: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    JWT_ALGORITHM: str
    JWT_SECRET_KEY: str
    DEBUG: bool = False

    # Stateless HMAC-based OTP (forgot-password flow).
    # High-entropy secret (>= 256 bits) — never hardcode, never log.
    OTP_SERVER_SECRET: str
    OTP_WINDOW_SECONDS: int = 300
    OTP_DIGITS: int = 6

    SMTP_HOST: str | None = None
    SMTP_PORT: int = 587
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    SMTP_FROM: str | None = None

    @field_validator("MODELS_NAME", mode="before")
    @classmethod
    def _parse_models(cls, v: Any) -> list[str]:
        return parse_comma_separated_list(v)

    @field_validator("OTP_SERVER_SECRET")
    @classmethod
    def _validate_otp_secret(cls, v: str) -> str:
        # Require at least 256 bits of entropy. A hex/base64-encoded
        # random value of >= 32 chars comfortably clears that bar.
        if len(v) < 32:
            raise ValueError(
                "OTP_SERVER_SECRET must be a high-entropy value "
                "of at least 32 characters (>= 256 bits)"
            )
        return v

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
