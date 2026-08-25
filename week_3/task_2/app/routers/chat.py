from collections.abc import AsyncIterable

import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.sse import EventSourceResponse, ServerSentEvent
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_db
from app.schemas import PromptIn, PromptOut
from app.services import ChatService

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/ask", response_model=PromptOut)
async def call_chat(
    msg: PromptIn,
    db: AsyncSession = Depends(get_db),
) -> PromptOut:

    messages = [
        {
            "role": "user",
            "content": msg.text,
        }
    ]

    service = ChatService(db=db)

    try:
        response = await service.get_chat_completion(messages)

        reply = response["choices"][0]["message"]["content"]
        model = response.get("model")

        conversation_id = await service.persist_exchange(
            user_id=msg.user_id,
            conversation_id=msg.conversation_id,
            user_message=msg.text,
            assistant_message=reply,
            model=model or "",
        )

        await db.commit()

        return PromptOut(
            conversation_id=conversation_id,
            reply=reply,
            model=model,
        )

    except httpx.HTTPStatusError as exc:
        await db.rollback()

        raise HTTPException(
            status_code=exc.response.status_code,
            detail=f"OpenRouter API error: {exc.response.text}",
        )

    except Exception as exc:
        await db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )


@router.post("/stream", response_class=EventSourceResponse)
async def stream_chat(
    msg: PromptIn,
    db: AsyncSession = Depends(get_db),
) -> EventSourceResponse:

    messages = [
        {
            "role": "user",
            "content": msg.text,
        }
    ]

    service = ChatService(db=db)

    async def event_generator():
        full_reply = ""

        try:
            async for token in service.stream_chat_completion(messages):
                full_reply += token

                yield ServerSentEvent(
                    data=token,
                    event="token",
                )

            # Only persist after successful completion
            conversation_id = await service.persist_exchange(
                user_id=msg.user_id,
                conversation_id=msg.conversation_id,
                user_message=msg.text,
                assistant_message=full_reply,
                model="",
            )

            await db.commit()

            yield ServerSentEvent(
                data=str(conversation_id),
                event="conversation_id",
            )

            yield ServerSentEvent(
                data="[DONE]",
                event="done",
            )

        except httpx.HTTPStatusError as exc:

            await db.rollback()

            yield ServerSentEvent(
                data=f"OpenRouter API error: {exc.response.text}",
                event="error",
            )

        except Exception as exc:

            await db.rollback()

            yield ServerSentEvent(
                data=str(exc),
                event="error",
            )

    return EventSourceResponse(event_generator())