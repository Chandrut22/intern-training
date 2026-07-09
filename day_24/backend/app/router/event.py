import asyncio
import os
import httpx
from fastapi.sse import EventSourceResponse
from fastapi import APIRouter

router = APIRouter()

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

    await queue.put({"event": "started", "data": f"{name} download started"})

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.get(url)
            response.raise_for_status()

            filename = name.replace(" ", "_")

            with open(f"downloads/{filename}", "wb") as file:
                file.write(response.content)

        await queue.put({"event": "completed", "data": f"{name} download completed"})

    except Exception as e:
        await queue.put({"event": "error", "data": f"{name} failed: {str(e)}"})


async def start_downloads():

    tasks = [asyncio.create_task(download_file(name, url)) for name, url in FILES]

    await asyncio.gather(*tasks)

    await queue.put({"event": "finished", "data": "All downloads completed"})


async def event_generator():

    asyncio.create_task(start_downloads())

    while True:
        message = await queue.get()

        yield f"event: {message['event']}\ndata: {message['data']}\n\n"

        if message["event"] == "finished":
            break


@router.get("/events")
async def events():
    return EventSourceResponse(event_generator())
