from jose import JWTError, jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from app.database.database import get_db
from app.model.user import User

from fastapi import WebSocket

from app.utils.jwt import (
    SECRET_KEY,
    ALGORITHM,
)


def get_current_user_websocket(websocket: WebSocket,db: Session) -> User:

    token = websocket.query_params.get("token")

    if token is None:
        raise Exception("Missing token")

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise Exception("Invalid token")

    except JWTError:
        raise Exception("Invalid token")

    user = (
        db.query(User)
        .filter(User.id == int(user_id))
        .first()
    )

    if user is None:
        raise Exception("User not found")

    return user



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = (
        db.query(User)
        .filter(User.id == int(user_id))
        .first()
    )

    if user is None:
        raise credentials_exception

    return user