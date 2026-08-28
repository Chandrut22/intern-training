from uuid import UUID

from app.models.messages import Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class MessageRepository:
    @staticmethod
    async def create(
        db: AsyncSession,
        conversation_id: UUID,
        role: str,
        content: str,
        model: str | None = None,
    ) -> Message:

        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            model=model,
        )

        db.add(message)
        await db.flush()

        return message

    @staticmethod
    async def get_by_conversation(
        db: AsyncSession,
        conversation_id: UUID,
    ) -> list[Message]:

        result = await db.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)
        )

        return list(result.scalars().all())
