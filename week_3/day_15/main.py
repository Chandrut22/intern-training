
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.sse import EventSourceResponse
import asyncio
import os
import httpx
import uvicorn

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")

# ----------------------------------------------------------------------------------------------------------------------


queue = asyncio.Queue()

os.makedirs("downloads", exist_ok=True)

FILES = [
    (
        "Python Guide",
        "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
    ),
    (
        "Sample Image",
        "https://picsum.photos/800/600",
    ),
    (
        "Sample JSON",
        "https://jsonplaceholder.typicode.com/posts",
    ),
]


async def download_file(name: str, url: str):

    await queue.put({
        "event": "started",
        "data": f"{name} download started"
    })

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.get(url)
            response.raise_for_status()

            filename = name.replace(" ", "_")

            with open(f"downloads/{filename}", "wb") as file:
                file.write(response.content)

        await queue.put({
            "event": "completed",
            "data": f"{name} download completed"
        })

    except Exception as e:
        await queue.put({
            "event": "error",
            "data": f"{name} failed: {str(e)}"
        })


async def start_downloads():

    tasks = [
        asyncio.create_task(download_file(name, url))
        for name, url in FILES
    ]

    await asyncio.gather(*tasks)

    await queue.put({
        "event": "finished",
        "data": "All downloads completed"
    })


async def event_generator():

    asyncio.create_task(start_downloads())

    while True:
        message = await queue.get()

        yield f"event: {message['event']}\ndata: {message['data']}\n\n"

        if message["event"] == "finished":
            break


@app.get("/events")
async def events():
    return EventSourceResponse(event_generator())


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)