from datetime import datetime
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import relationship

try:
    from app.database.database import Base
except ModuleNotFoundError:
    print("Module not found")


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(Integer, unique=True, nullable=False)

    created_at = Column(DateTime, default=datetime.now)

    messages = relationship(
        "ChatMessage", back_populates="session", cascade="all, delete"
    )
