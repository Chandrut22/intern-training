from typing import Annotated

from fastapi import (
    APIRouter,
    Request,
    Depends,
    HTTPException,
    Response,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.core.config import settings
from app.schemas.auth import (
    CreateAccountRequest,
    ForgotPasswordRequest,
    LoginRequest,
    MessageResponse,
    ResetPasswordRequest,
    TokenResponse,
    UserResponse,
)
from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_account(
    data: CreateAccountRequest,
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
):
    service = AuthService(db)

    user = await service.create_account(data)

    return UserResponse(
        id=str(user.id),
        email=user.email,
        username=user.username,
        role=user.role,
    )


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    data: LoginRequest,
    response: Response,
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
):
    service = AuthService(db)

    tokens = await service.login(data)

    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        secure=False,  
        samesite="lax",
        max_age=(60* 60 * 24 * settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )

    return {
        "access_token": tokens["access_token"],
        "token_type": tokens["token_type"],
    }

@router.post(
    "/refresh",
    response_model=TokenResponse,
)
async def refresh_access_token(
    request: Request,
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
):
    refresh_token = request.cookies.get(
        "refresh_token"
    )

    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found",
        )

    service = AuthService(db)

    return await service.refresh_access_token(
        refresh_token
    )


@router.post(
    "/forgot-password/request",
    response_model=MessageResponse,
)
async def request_otp(
    data: ForgotPasswordRequest,
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
):
    service = AuthService(db)

    return await service.request_otp(data)


@router.post(
    "/reset-password",
    response_model=MessageResponse,
)
async def reset_password(
    data: ResetPasswordRequest,
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
):
    service = AuthService(db)

    return await service.reset_password(data)