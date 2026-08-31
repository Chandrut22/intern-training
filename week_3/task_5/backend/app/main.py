from fastapi import FastAPI

from app.routers.auth_router import router as auth_router
from app.routers.chat_router import router as chat_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(chat_router)


@app.get("/")
def root():
    return {"msg": "Hello World"}
