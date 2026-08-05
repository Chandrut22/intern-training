from sqlalchemy.orm import Session

from model.chat_message import ChatMessage
from model.chat_session import ChatSession


def get_session(db: Session, session_id: int):
    return db.query(ChatSession).filter(ChatSession.session_id == session_id).first()


def create_session(db: Session, session_id: int):
    session = ChatSession(session_id=session_id)

    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_or_create_session(db: Session,session_id: int):
    session = get_session(db,session_id)

    if session is None:
        session = create_session(db,session_id)

    return session


def save_message(db: Session, session_id: int, user_id: int, message: str ):
    chat_message = ChatMessage(session_id=session_id, user_id=user_id, message=message)

    db.add(chat_message)
    db.commit()
    db.refresh(chat_message)
    return chat_message


def get_chat_history(db: Session, session_id: int):
    return db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at.asc()).all()
    