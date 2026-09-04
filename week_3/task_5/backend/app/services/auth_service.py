import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.otp_service import generate_otp, verify_otp as verify_otp_code
from app.core.security import (
    hash_password,
    verify_password,
)
from app.repositories.user_repo import UserRepository
from app.schemas.auth import (
    CreateAccountRequest,
    ForgotPasswordRequest,
    LoginRequest,
    ResetPasswordRequest,
)
from app.core.security import JWTService
from app.services.email_service import EmailService


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.users = UserRepository(db)

    async def create_account(
        self,
        data: CreateAccountRequest,
    ):
        existing_email = await self.users.get_by_email(data.email)

        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        existing_username = await self.users.get_by_username(data.username)

        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already taken",
            )

        password_hash = hash_password(data.password)

        user = await self.users.create(
            email=data.email,
            username=data.username,
            password_hash=password_hash,
        )

        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def login(
        self,
        data: LoginRequest,
    ):
        user = await self.users.get_by_email(data.email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not verify_password(
            data.password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        access_token = JWTService.create_access_token(user.id, user.role)

        refresh_token = JWTService.create_refresh_token(user.id)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    async def refresh_access_token(
        self,
        refresh_token: str,
    ):
        try:
            payload = JWTService.decode_token(refresh_token)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(exc),
            )

        # Make sure this is a refresh token
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )

        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )

        try:
            user_uuid = uuid.UUID(user_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user ID",
            )

        # Optional but recommended:
        # Make sure the user still exists.
        user = await self.users.get_by_id(user_uuid)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        access_token = JWTService.create_access_token(user.id, user.role)

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }

    async def request_otp(
        self,
        data: ForgotPasswordRequest,
    ):
        user = await self.users.get_by_email(data.email)

        # Always return the same message regardless of whether the
        # email is registered, so this endpoint can't be used to
        # enumerate accounts. The OTP is only actually generated and
        # sent when the user exists.
        if user:
            otp = generate_otp(user.email, user.password_hash)

            EmailService.send_otp_email(user.email, otp)

        return {
            "message": "If that email is registered, an OTP has been sent to it.",
        }

    async def reset_password(
        self,
        data: ResetPasswordRequest,
    ):
        user = await self.users.get_by_email(data.email)

        if not user or not verify_otp_code(
            user.email,
            data.otp,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired OTP",
            )

        user.password_hash = hash_password(data.new_password)

        await self.db.commit()

        return {
            "message": "Password has been reset successfully.",
        }
