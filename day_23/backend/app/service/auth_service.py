from sqlalchemy.orm import Session

from app.model.user import User
from app.schemas.auth import RegisterRequest, LoginRequest
from app.utils.security import hash_password, verify_password
from app.utils.jwt import create_access_token


def get_user_by_email(db: Session, email: str):
    return (db.query(User).filter(User.email == email).first())

def get_user_by_id(db: Session, user_id: int):
    return (db.query(User).filter(User.id == user_id).first())

def register_user(db: Session,request: RegisterRequest):
    existing_user = get_user_by_email(db,request.email)
    if existing_user is not None: raise ValueError("Email already exist")

    hashed = hash_password(request.password)
    user = User(username = request.username, email=request.email, password = hashed)
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def login_user(db: Session, request: LoginRequest):
    user = get_user_by_email(db,request.email)
    if user is None: raise ValueError("Invalid User credentials")
    
    valid = verify_password(request.password, user.password)

    if not valid: raise ValueError("Invalid Password credentials")
    token = create_access_token(user.id)
    return {
        "access_token" : token,
        "token_type" : "bearer"
    }


