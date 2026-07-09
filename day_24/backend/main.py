from fastapi import FastAPI
from app.router.socket import router as websocket_router
from app.router.event import router as sse_router
from app.router.auth import router as auth_router
from app.router.chatbot import router as chat_router
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(websocket_router)
app.include_router(sse_router)
app.include_router(auth_router)
app.include_router(chat_router)


@app.get("/")
def home():
    return {"message": "Chat Application API"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
