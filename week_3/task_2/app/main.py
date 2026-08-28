import logging
import uuid

from app.core.logging import RequestIDFilter
from app.core.request_context import request_id_ctx
from app.routers.chat import router as chat_router
from fastapi import FastAPI, Request

app = FastAPI()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | request_id=%(request_id)s | %(message)s",
)

for handler in logging.getLogger().handlers:
    handler.addFilter(RequestIDFilter())


@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    token = request_id_ctx.set(request_id)
    try:
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
    finally:
        request_id_ctx.reset(token)


app.include_router(chat_router)


@app.get("/")
def root():
    return {"message": "Hello World"}
