import uuid

from app.database.db import Base
from sqlalchemy import UUID, DateTime, String, func
from sqlalchemy.orm import mapped_column, relationship


class Conversation(Base):
    __tablename__ = "conversations"

    id = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    title = mapped_column(
        String(255),
        nullable=True,
    )

    created_at = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    messages = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan",
    )
