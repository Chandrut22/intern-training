import uuid

from collections.abc import AsyncGenerator

from fastapi import HTTPException

from app.db.database import SessionLocal
from app.models import Conversation
from app.repositories.conversation_repo import ConversationRepository
from app.repositories.message_repo import MessageRepository
from app.services.llm_service import LLMService


class ChatService:

    def __init__(self):
        self.llm_service = LLMService()

    # =========================================================
    # Normal chat
    # =========================================================

    async def chat(
        self,
        user_id: uuid.UUID,
        message: str,
        conversation_id: uuid.UUID | None = None,
    ):

        async with SessionLocal() as db:

            conversations = ConversationRepository(db)
            messages = MessageRepository(db)

            try:

                # ---------------------------------------------
                # 1. Get existing conversation
                # ---------------------------------------------

                conversation = None

                if conversation_id is not None:

                    conversation = await conversations.get_by_id_for_user(
                        conversation_id, user_id
                    )

                # ---------------------------------------------
                # 2. Create new conversation if none found
                # ---------------------------------------------
                # A missing/foreign conversation_id falls back to
                # starting a new conversation instead of erroring.

                if conversation is None:

                    conversation = await conversations.create(
                        user_id=user_id,
                        title=message[:100],
                    )

                # ---------------------------------------------
                # 3. Save user message
                # ---------------------------------------------

                await messages.create(
                    conversation_id=conversation.id,
                    role="user",
                    content=message,
                )

                # ---------------------------------------------
                # 4. Generate LLM response
                # ---------------------------------------------

                ai_message = await self.llm_service.generate(
                    message
                )

                usage = ai_message.usage_metadata or {}

                # ---------------------------------------------
                # 5. Save assistant message
                # ---------------------------------------------

                await messages.create(
                    conversation_id=conversation.id,
                    role="assistant",
                    content=ai_message.content,
                    model=self.llm_service.model_name,
                    prompt_tokens=usage.get("input_tokens"),
                    completion_tokens=usage.get("output_tokens"),
                    total_tokens=usage.get("total_tokens"),
                )

                # ---------------------------------------------
                # 6. Commit
                # ---------------------------------------------

                await db.commit()

                # ---------------------------------------------
                # 7. Return response
                # ---------------------------------------------

                return {
                    "conversation_id": conversation.id,
                    "message": ai_message.content,
                }

            except HTTPException:
                await db.rollback()
                raise

            except Exception:
                await db.rollback()
                raise

    # =========================================================
    # Streaming chat
    # =========================================================

    async def stream_chat(
        self,
        user_id: uuid.UUID,
        message: str,
        conversation_id: uuid.UUID | None = None,
    ) -> AsyncGenerator[dict, None]:

        async with SessionLocal() as db:

            conversations = ConversationRepository(db)
            messages = MessageRepository(db)

            try:

                # ---------------------------------------------
                # 1. Get existing conversation
                # ---------------------------------------------

                conversation = None

                if conversation_id is not None:

                    conversation = await conversations.get_by_id_for_user(
                        conversation_id, user_id
                    )

                # ---------------------------------------------
                # 2. Create conversation if none found
                # ---------------------------------------------
                # A missing/foreign conversation_id falls back to
                # starting a new conversation instead of erroring.

                if conversation is None:

                    conversation = await conversations.create(
                        user_id=user_id,
                        title=message[:100],
                    )

                # ---------------------------------------------
                # 3. Save user message
                # ---------------------------------------------

                await messages.create(
                    conversation_id=conversation.id,
                    role="user",
                    content=message,
                )

                # ---------------------------------------------
                # 4. Send conversation ID
                # ---------------------------------------------

                yield {
                    "type": "conversation",
                    "conversation_id": str(
                        conversation.id
                    ),
                }

                # ---------------------------------------------
                # 5. Stream LLM response
                # ---------------------------------------------

                full_response: list[str] = []

                async for chunk in self.llm_service.stream(
                    message
                ):

                    if not chunk:
                        continue

                    full_response.append(chunk)

                    yield {
                        "type": "token",
                        "conversation_id": str(
                            conversation.id
                        ),
                        "content": chunk,
                    }

                # ---------------------------------------------
                # 6. Combine response
                # ---------------------------------------------

                assistant_content = "".join(
                    full_response
                )

                usage = self.llm_service.last_usage_metadata or {}

                # ---------------------------------------------
                # 7. Save assistant message
                # ---------------------------------------------

                await messages.create(
                    conversation_id=conversation.id,
                    role="assistant",
                    content=assistant_content,
                    model=self.llm_service.model_name,
                    prompt_tokens=usage.get("input_tokens"),
                    completion_tokens=usage.get("output_tokens"),
                    total_tokens=usage.get("total_tokens"),
                )

                # ---------------------------------------------
                # 8. Commit
                # ---------------------------------------------

                await db.commit()

                # ---------------------------------------------
                # 9. Send done event
                # ---------------------------------------------

                yield {
                    "type": "done",
                    "conversation_id": str(
                        conversation.id
                    ),
                }

            except Exception:
                await db.rollback()
                raise

    # =========================================================
    # List conversations
    # =========================================================

    async def get_conversations(
        self,
        user_id: uuid.UUID,
    ) -> list[Conversation]:

        async with SessionLocal() as db:

            conversations = ConversationRepository(db)

            return await conversations.list_for_user_with_messages(
                user_id
            )