import json
import logging
from collections.abc import AsyncIterable

import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential_jitter,
)

from app.core.settings import settings
from app.repositories.conversation_repo import ConversationRepository
from app.repositories.message_repo import MessageRepository
from app.repositories.user_repo import UserRepository

from sqlalchemy.dialects.postgresql import UUID

logger = logging.getLogger(__name__)


class ChatService:

    def __init__(self, db: AsyncSession | None = None):
        self.url = str(settings.OPENROUTER_BASE_URL)
        self.headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }
        self.db = db

    @retry(
        retry=retry_if_exception_type((httpx.RequestError, httpx.HTTPStatusError)),
        wait=wait_exponential_jitter(initial=2, max=10, jitter=1),
        stop=stop_after_attempt(5),
        reraise=True,
        before_sleep=lambda retry_state: logger.warning(
            f"API request failed. Retrying in {retry_state.next_action.sleep} seconds..."
        ),
    )
    async def _post_once(self, payload: dict) -> httpx.Response:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                self.url,
                headers=self.headers,
                json=payload,
            )
            response.raise_for_status()
            return response

    def _build_payload(
        self,
        models: list[str],
        messages: list[dict[str, str]],
        temperature: float,
        max_token: int,
        stream: bool = False,
    ) -> dict:
        return {
            "models": models,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_token,
            "stream": stream,
        }

    async def get_chat_completion(
        self,
        messages: list[dict[str, str]],
        temperature: float = settings.TEMPERATURE,
        max_token: int = settings.MAX_TOKEN,
    ) -> dict:
        model_list = list(settings.MODELS_NAME)
        if not model_list:
            raise ValueError("No models configured — set MODELS_NAME in .env")

        payload = self._build_payload(model_list, messages, temperature, max_token)

        try:
            response = await self._post_once(payload)
            logger.info("Chat completion succeeded")
            return response.json()
        except httpx.HTTPStatusError as exc:
            logger.warning("OpenRouter failed with HTTP %s", exc.response.status_code)
            raise
        except httpx.RequestError as exc:
            logger.error("Network error calling OpenRouter: %s", exc)
            raise

    async def stream_chat_completion(
        self,
        messages: list[dict[str, str]],
        temperature: float = settings.TEMPERATURE,
        max_token: int = settings.MAX_TOKEN,
    ) -> AsyncIterable[str]:
        model_list = list(settings.MODELS_NAME)
        if not model_list:
            raise ValueError("No models configured — set MODELS_NAME in .env")


        payload = self._build_payload(model_list, messages, temperature, max_token, stream=True)

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                async with client.stream(
                    "POST",
                    self.url,
                    headers=self.headers,
                    json=payload,
                ) as response:
                    response.raise_for_status()
                    logger.info("Starting OpenRouter stream")

                    async for line in response.aiter_lines():
                        if not line or not line.startswith("data:"):
                            continue

                        data = line[len("data:"):].strip()

                        if data == "[DONE]":
                            return

                        try:
                            chunk = json.loads(data)
                        except json.JSONDecodeError:
                            logger.warning("Skipping malformed SSE chunk")
                            continue

                        delta = (
                            chunk.get("choices", [{}])[0]
                            .get("delta", {})
                            .get("content")
                        )

                        if delta:
                            yield delta
        except httpx.HTTPStatusError as exc:
            logger.warning(
                "OpenRouter stream failed with HTTP %s",
                exc.response.status_code,
            )
            raise
        except httpx.RequestError as exc:
            logger.error("Network error opening stream: %s", exc)
            raise

    async def persist_exchange(
        self,
        *,
        user_id: UUID,
        conversation_id: UUID | None,
        user_message: str,
        assistant_message: str,
        model: str,
    ):
        if self.db is None:
            return conversation_id

        # 1. Check user
        user = await UserRepository.get_by_id(
            self.db,
            user_id,
        )

        if user is None:
            raise ValueError(
                f"User {user_id} does not exist"
            )

        # 2. Conversation doesn't exist → create it
        if conversation_id is None:

            conversation = await ConversationRepository.create(
                self.db,
                user_id=user_id,
                title=user_message[:80] or None,
            )

            conversation_id = conversation.id

        # 3. Conversation was provided → verify it
        else:

            conversation = await ConversationRepository.get_by_id(
                self.db,
                conversation_id,
            )

            if conversation is None:
                raise ValueError(
                    f"Conversation {conversation_id} does not exist"
                )

            # Important: make sure this conversation belongs
            # to the current user.
            if conversation.user_id != user_id:
                raise ValueError(
                    "Conversation does not belong to this user"
                )

        # 4. Save user message
        await MessageRepository.create(
            self.db,
            conversation_id=conversation_id,
            role="user",
            content=user_message,
        )

        # 5. Save assistant response
        await MessageRepository.create(
            self.db,
            conversation_id=conversation_id,
            role="assistant",
            content=assistant_message,
            model=model,
        )

        return conversation_id