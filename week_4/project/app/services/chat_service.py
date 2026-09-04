from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.conversation_repo import ConversationRepository
from app.repositories.message_repo import MessageRepository
from app.rag.llm import run_rag_chain, stream_rag_chain
from langchain_core.messages import HumanMessage, AIMessage

class ChatService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.conversation_repo = ConversationRepository(db)
        self.message_repo = MessageRepository(db)

    async def get_conversation_history(self, conversation_id):
        messages = await self.message_repo.get_history(conversation_id)
        history = []
        for msg in messages:
            if msg.role == "user":
                history.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                history.append(AIMessage(content=msg.content))
        return history

    async def get_chat_completion(self, input_text: str, conversation_id=None):
        history = []
        if conversation_id:
            history = await self.get_conversation_history(conversation_id)

        # Invoke the RAG chain
        response = await run_rag_chain(input_text,history)

        # The rag_chain in llm.py ends with StrOutputParser(), so it returns a string.
        # However, chat_router.py expects a dictionary like OpenRouter/OpenAI response.
        # I will return a compatible structure.
        return {
            "choices": [
                {
                    "message": {
                        "content": response
                    }
                }
            ],
            "model": "openai/gpt-oss-20b" # Hardcoded to match rag_chain's model
        }

    async def stream_chat_completion(self, input_text: str, conversation_id=None):
        history = []
        if conversation_id:
            history = await self.get_conversation_history(conversation_id)

        async for token in stream_rag_chain(input_text, history):
            yield token

    async def persist_exchange(self, conversation_id, user_message, assistant_message, model):
        # Ensure conversation exists
        if not conversation_id:
            conversation = await self.conversation_repo.create()
            conversation_id = conversation.id
        else:
            conversation = await self.conversation_repo.get_by_id(conversation_id)
            if not conversation:
                conversation = await self.conversation_repo.create()
                conversation_id = conversation.id

        # Save user message
        await self.message_repo.create(
            conversation_id=conversation_id,
            role="user",
            content=user_message
        )

        # Save assistant message
        await self.message_repo.create(
            conversation_id=conversation_id,
            role="assistant",
            content=assistant_message,
            model=model
        )

        return conversation_id
