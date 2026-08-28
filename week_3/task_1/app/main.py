from app.routers.chat import router as chat_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(chat_router)


@app.get("/")
def root():
    return "Hello World"
