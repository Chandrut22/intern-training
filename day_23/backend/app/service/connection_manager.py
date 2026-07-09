from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, session_id: int, websocket: WebSocket):
        await websocket.accept()

        if session_id not in self.active_connections:
            self.active_connections[session_id] = []

        self.active_connections[session_id].append(websocket)

    def disconnect(self, session_id: int, websocket: WebSocket):
        if session_id in self.active_connections:
            self.active_connections[session_id].remove(websocket)

            if not self.active_connections[session_id]:
                del self.active_connections[session_id]

    async def send_personal_message(self, websocket: WebSocket, message: dict):
        await websocket.send_json(message)

    async def broadcast(self, session_id: int, message: dict):
        if session_id in self.active_connections:
            for connection in self.active_connections[session_id]:
                await connection.send_json(message)


manager = ConnectionManager()