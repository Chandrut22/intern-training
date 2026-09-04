from uuid import UUID

from pydantic import BaseModel


class PromptIn(BaseModel):
    text: str
    conversation_id: UUID | None = None


class ChatMessage(BaseModel):
    role: str
    content: str


class PromptOut(BaseModel):
    conversation_id: UUID
    reply: str
    model: str | None = None
