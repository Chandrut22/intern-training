from collections.abc import AsyncGenerator

from langchain.chat_models import init_chat_model
from langchain.messages import AIMessage, HumanMessage

from app.core.config import settings


class LLMService:
    def __init__(self):

        self.model_name = settings.MODELS_NAME[1]

        self.llm = init_chat_model(
            model_provider="openrouter",
            model=self.model_name,
            api_key=settings.OPENROUTER_API_KEY,
            temperature=settings.TEMPERATURE,
            max_tokens=settings.MAX_TOKEN,
        )

        # Populated after `stream()` has been fully consumed, since
        # an async generator can't also return a value.
        self.last_usage_metadata: dict | None = None

    # =========================================================
    # Normal generation
    # =========================================================

    async def generate(
        self,
        message: str,
    ) -> AIMessage:

        return await self.llm.ainvoke([HumanMessage(content=message)])

    # =========================================================
    # Streaming generation
    # =========================================================

    async def stream(
        self,
        message: str,
    ) -> AsyncGenerator[str, None]:

        self.last_usage_metadata = None
        full_message: AIMessage | None = None

        async for chunk in self.llm.astream([HumanMessage(content=message)]):
            full_message = chunk if full_message is None else full_message + chunk

            if chunk.content:
                yield chunk.content

        if full_message is not None:
            self.last_usage_metadata = full_message.usage_metadata
