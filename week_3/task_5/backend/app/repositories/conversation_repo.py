import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Conversation


class ConversationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id_for_user(
        self,
        conversation_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> Conversation | None:

        result = await self.db.execute(
            select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id,
            )
        )

        return result.scalar_one_or_none()

    async def create(
        self,
        user_id: uuid.UUID,
        title: str | None,
    ) -> Conversation:

        conversation = Conversation(
            user_id=user_id,
            title=title,
        )

        self.db.add(conversation)

        await self.db.flush()

        return conversation

    async def list_for_user_with_messages(
        self,
        user_id: uuid.UUID,
    ) -> list[Conversation]:

        result = await self.db.execute(
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .options(selectinload(Conversation.messages))
            .order_by(Conversation.created_at.desc())
        )

        conversations = result.scalars().all()

        for conversation in conversations:
            conversation.messages.sort(key=lambda m: m.created_at)

        return list(conversations)
