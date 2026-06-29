from fastapi import WebSocket, WebSocketDisconnect, APIRouter

from database.database import SessionLocal
from service.chat_service import (
    get_or_create_session,
    get_chat_history,
    save_message
)
from service.connection_manager import manager

router = APIRouter()


@router.websocket("/chat/{session_id}")
async def chat(
    websocket: WebSocket,
    session_id: int,
    user_id: int
):
    print("WebSocket endpoint reached")
    db = SessionLocal()

    await manager.connect(session_id, websocket)

    get_or_create_session(db, session_id)

    history = get_chat_history(db, session_id)

    await manager.send_personal_message(
        websocket,
        {
            "type": "history",
            "messages": [
                {
                    "user_id": msg.user_id,
                    "message": msg.message,
                    "created_at": msg.created_at.isoformat()
                }
                for msg in history
            ]
        }
    )

    try:

        while True:

            text = await websocket.receive_text()

            message = save_message(db, session_id, user_id, text)

            await manager.broadcast(
                session_id,
                {
                    "type": "message",
                    "user_id": message.user_id,
                    "message": message.message,
                    "created_at": message.created_at.isoformat()
                }
            )

    except WebSocketDisconnect:

        manager.disconnect(
            session_id,
            websocket
        )

        db.close()
