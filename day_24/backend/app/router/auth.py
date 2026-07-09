from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
)
from app.service.auth_service import (
    register_user,
    login_user,
)

from app.utils.dependency import get_current_user

from app.model.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    try:
        user = register_user(db, request)

        return {
            "message": "User registered successfully",
            "user_id": user.id,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    try:
        token = login_user(db, request)
        return token

    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user),
):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
    }
