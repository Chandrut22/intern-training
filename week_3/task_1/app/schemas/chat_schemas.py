from pydantic import BaseModel


class PromptIn(BaseModel):
    text: str


class PromptOut(BaseModel):
    text: str


class ChatMessage(BaseModel):
    role: str
    content: str
