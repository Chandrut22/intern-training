from collections.abc import AsyncIterable

import httpx
from app.schemas import ChatMessage, PromptIn
from app.services import ChatService
from fastapi import APIRouter, HTTPException, status
from fastapi.sse import EventSourceResponse, ServerSentEvent

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/ask")
async def call_chat(msg: PromptIn) -> list[ChatMessage]:

    try:
        messages = [{"role": "user", "content": msg.text}]
        response = await ChatService().get_chat_completion(messages)
        messages.append(
            {
                "role": "assistant",
                "content": response["choices"][0]["message"]["content"],
            }
        )
        return [ChatMessage(**m) for m in messages]

    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=f"OpenRouter API error: {exc.response.text}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/stream", response_class=EventSourceResponse)
async def stream_chat(msg: PromptIn) -> AsyncIterable[ServerSentEvent]:

    messages = [{"role": "user", "content": msg.text}]
    service = ChatService()
    try:
        async for token in service.stream_chat_completion(messages):
            yield ServerSentEvent(data=token, event="token")
    except httpx.HTTPStatusError as exc:
        yield ServerSentEvent(
            data=f"OpenRouter API error: {exc.response.text}",
            event="error",
        )
    except Exception as e:
        yield ServerSentEvent(data=str(e), event="error")
    finally:
        yield ServerSentEvent(raw_data="[DONE]", event="done")
