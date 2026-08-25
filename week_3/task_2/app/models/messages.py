from app.database.db import Base
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import UUID, ForeignKey, String, Text, DateTime, func
import uuid

class Message(Base):
    __tablename__ = "messages"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    conversation_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
    )

    role = mapped_column(String(20), nullable=False)
    content = mapped_column(Text, nullable=False)
    model = mapped_column(String(100), nullable=True)

    created_at = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    conversation = relationship(
        "Conversation",
        back_populates="messages",
    )