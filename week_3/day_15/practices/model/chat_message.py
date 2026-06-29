
from datetime import datetime
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey

from sqlalchemy.orm import relationship

try:
    from practices.database.database import Base
except ModuleNotFoundError:
    print("Module not found")

try:
    from database.database import Base
except ModuleNotFoundError:
    print("Module not found")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(Integer, ForeignKey("chat_sessions.session_id"), nullable=False)

    user_id = Column(Integer, nullable=False)

    message = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.now)

    session = relationship("ChatSession",back_populates="messages")