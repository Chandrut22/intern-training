from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.database.database import SessionLocal
from app.service.chat_service import (
    get_or_create_session,
    get_chat_history,
    save_message,
)
from app.service.connection_manager import manager
from app.utils.dependency import get_current_user_websocket

router = APIRouter()


@router.websocket("/chat/{session_id}")
async def chat(
    websocket: WebSocket,
    session_id: int,
):
    print("WebSocket endpoint reached")

    db = SessionLocal()

    try:
        current_user = get_current_user_websocket(
            websocket=websocket,
            db=db,
        )

        await manager.connect(
            session_id,
            websocket,
        )

        get_or_create_session(
            db,
            session_id,
        )

        history = get_chat_history(
            db,
            session_id,
        )

        await manager.send_personal_message(
            websocket,
            {
                "type": "history",
                "messages": [
                    {
                        "user_id": message.user_id,
                        "message": message.message,
                        "created_at": message.created_at.isoformat(),
                    }
                    for message in history
                ],
            },
        )

        while True:

            text = await websocket.receive_text()

            saved_message = save_message(
                db=db,
                session_id=session_id,
                user_id=current_user.id,
                message=text,
            )

            await manager.broadcast(
                session_id,
                {
                    "type": "message",
                    "user_id": saved_message.user_id,
                    "message": saved_message.message,
                    "created_at": saved_message.created_at.isoformat(),
                },
            )

    except WebSocketDisconnect:
        manager.disconnect(
            session_id,
            websocket,
        )

    except Exception as e:
        print(f"WebSocket Error: {e}")

        await websocket.close(code=1008)

    finally:
        db.close()
