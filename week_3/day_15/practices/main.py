from fastapi import FastAPI
from router.socket import router as websocket_router

app = FastAPI()

app.include_router(websocket_router)

@app.get("/")
def home():
    return {
        "message": "Chat Application API"
    }
