from uuid import UUID

from app.models.conversations import Conversation
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class ConversationRepository:
    @staticmethod
    async def create(
        db: AsyncSession,
        user_id: UUID,
        title: str | None = None,
    ) -> Conversation:

        conversation = Conversation(
            user_id=user_id,
            title=title,
        )

        db.add(conversation)
        await db.flush()

        return conversation

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        conversation_id: UUID,
    ) -> Conversation | None:

        result = await db.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )

        return result.scalar_one_or_none()
