from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.conversations import Conversation

class ConversationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, conversation_id):
        result = await self.db.execute(select(Conversation).where(Conversation.id == conversation_id))
        return result.scalar_one_or_none()

    async def create(self, title: str | None = None):
        conversation = Conversation(title=title)
        self.db.add(conversation)
        await self.db.flush()
        return conversation
