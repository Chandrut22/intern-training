from fastapi import FastAPI
from router.socket import router as websocket_router
import uvicorn

app = FastAPI()

app.include_router(websocket_router)

@app.get("/")
def home():
    return {
        "message": "Chat Application API"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)