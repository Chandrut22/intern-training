from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.messages import Message

class MessageRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, conversation_id, role: str, content: str, model: str | None = None):
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            model=model
        )
        self.db.add(message)
        await self.db.flush()
        return message

    async def get_history(self, conversation_id):
        result = await self.db.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
        )
        return result.scalars().all()
