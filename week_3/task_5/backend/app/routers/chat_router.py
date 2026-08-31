import json

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.dependencies.auth import get_current_user
from app.models import User
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    ConversationWithMessagesResponse,
)
from app.services.chat_service import ChatService


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
)
async def chat(
    data: ChatRequest,
    current_user: User = Depends(get_current_user),
):
    service = ChatService()

    return await service.chat(
        user_id=current_user.id,
        message=data.message,
        conversation_id=data.conversation_id,
    )


@router.post("/stream")
async def stream_chat(
    data: ChatRequest,
    current_user: User = Depends(get_current_user),
):
    service = ChatService()

    async def event_generator():

        try:
            async for event in service.stream_chat(
                user_id=current_user.id,
                message=data.message,
                conversation_id=data.conversation_id,
            ):
                yield (
                    f"event: {event['type']}\n"
                    f"data: {json.dumps(event)}\n\n"
                )

        except Exception as exc:

            # HTTP status cannot be changed here because
            # StreamingResponse has already started.

            yield (
                "event: error\n"
                f"data: {json.dumps({'type': 'error', 'message': str(exc)})}\n\n"
            )

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.get(
    "/conversations",
    response_model=list[ConversationWithMessagesResponse],
)
async def list_conversations(
    current_user: User = Depends(get_current_user),
):
    service = ChatService()

    return await service.get_conversations(
        user_id=current_user.id
    )