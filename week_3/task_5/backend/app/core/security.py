from datetime import datetime, timedelta, timezone
import uuid

import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from app.core.config import settings

password_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return password_hasher.verify(password_hash, password)
    except VerifyMismatchError:
        return False


class JWTService:
    @staticmethod
    def create_access_token(user_id: uuid.UUID, role: str) -> str:
        now = datetime.now(timezone.utc)

        payload = {
            "sub": str(user_id),
            "role": role,
            "type": "access",
            "iat": now,
            "exp": now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        }

        return jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )

    @staticmethod
    def create_refresh_token(user_id: uuid.UUID) -> str:
        now = datetime.now(timezone.utc)

        payload = {
            "sub": str(user_id),
            "type": "refresh",
            "iat": now,
            "exp": now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        }

        return jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            return jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )

        except ExpiredSignatureError:
            raise ValueError("Token has expired")

        except InvalidTokenError:
            raise ValueError("Invalid token")
