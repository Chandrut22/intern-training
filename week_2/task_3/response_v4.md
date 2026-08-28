
# Prompt: give the program to chat to the llm in openrouter as API request using httpx and need to implement the async using gather and i need to stream the llm

## Response:
Below is a **stand‑alone, ready‑to‑run** example that shows how to

| ✅ | Feature |
|----|---------|
| 🔥 | Call OpenRouter’s chat‑completion endpoint as a **streaming** request |
| 🌐 | Use **httpx.AsyncClient** (no `aiohttp` needed) |
| 🚀 | Fire two independent streams in parallel with `asyncio.gather` |
| 🔀 | Consume the stream token‑by‑token and print it live |

> **Prerequisites**  
> ```bash
> pip install httpx==0.27.*
> export OPENROUTER_API_KEY="YOUR_OPENROUTER_KEY"   # or set it in your env
> ```

---

## 1️⃣ The complete script

```python
#!/usr/bin/env python3
"""async_stream_chat.py – Stream multiple LLM chat responses with httpx + asyncio"""

import os
import json
import asyncio
from typing import AsyncGenerator, List, Dict

import httpx

# --------------------------------------------------------------------------
# Configuration & helpers
# --------------------------------------------------------------------------

API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise RuntimeError(
        "Please set the OPENROUTER_API_KEY environment variable to your key."
    )

BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "openrouter/o1-mini"  # change to any supported model

HEADERS: Dict[str, str] = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    # OpenRouter distinguishes streaming by this accept header
    "Accept": "text/event-stream",
}


async def stream_chat(
    client: httpx.AsyncClient,
    messages: List[Dict[str, str]],
    *,
    model: str = MODEL,
    temperature: float = 0.7,
    top_p: float = 1.0,
) -> AsyncGenerator[str, None]:
    """
    Yield tokens (content strings) from the model as they arrive.

    :param client: Re‑used AsyncClient – share connections across calls
    :param messages: List of OpenAI‑style message dicts
    :param model: Model ID
    :param temperature: Sampler temperature
    :param top_p: Top‑p nucleus sampling
    :yield: ``str`` – a chunk of the generated text
    """
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "top_p": top_p,
        "stream": True,
    }

    # OpenRouter expects a streamed response as a Server‑Sent Events (SSE) stream.
    async with client.stream(
        "POST", f"{BASE_URL}/chat/completions", json=payload, headers=HEADERS
    ) as resp:
        resp.raise_for_status()

        async for line in resp.aiter_lines():
            if not line:
                continue
            # Each non‑empty line looks like: data: {"choices":[{"delta":{"content":"..."}},...}]
            if line.startswith("data: "):
                raw = line[6:].strip()
                if raw == "[DONE]":
                    break
                try:
                    data = json.loads(raw)
                except json.JSONDecodeError:
                    continue  # skip malformed lines

                # open router follows the ChatCompletionDelta schema
                for choice in data.get("choices", []):
                    delta = choice.get("delta", {})
                    if "content" in delta:
                        yield delta["content"]


# --------------------------------------------------------------------------
# Running several streams in parallel
# --------------------------------------------------------------------------


async def _print_stream(
    task: AsyncGenerator[str, None],  # the stream generator
    label: str,  # label for the console
) -> None:
    """Consume a stream and echo it to the console."""
    async for token in task:
        print(f"[{label}]: {token}", end="", flush=True)
    print("\n" + "-" * 40)


async def main() -> None:
    """
    Fire two independent chat streams and watch their output live.
    Feel free to replace the messages with your own prompts.
    """
    messages1 = [{"role": "user", "content": "Hello, how are you?"}]
    messages2 = [{"role": "user", "content": "Tell me a joke about cats."}]

    async with httpx.AsyncClient() as client:
        # Create stream generators but *don't* start consuming yet
        stream1 = stream_chat(client, messages1)
        stream2 = stream_chat(client, messages2)

        # Now run both streams concurrently
        await asyncio.gather(
            _print_stream(stream1, "Chat‑1"),
            _print_stream(stream2, "Chat‑2"),
        )


# --------------------------------------------------------------------------
# Entrypoint
# --------------------------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 2️⃣ How it works

| Step | What happens |
|------|--------------|
| **HTTP client** | `httpx.AsyncClient()` keeps an HTTP/2 connection pool open, so two requests reuse the same socket. |
| **Endpoint** | `POST /chat/completions` with `"stream": true`. |
| **Headers** | `Accept: text/event-stream` tells OpenRouter we want a Server‑Sent Events (SSE) stream. |
| **Streaming** | `client.stream()` returns an async context manager that yields each received network line via `aiter_lines()`. |
| **SSE parsing** | We strip the `"data: "` prefix, skip `"[DONE]"`, parse the JSON, and yield the `content` field from each `delta` object. |
| **Parallelism** | Two generator objects (`stream1`, `stream2`) are passed to `asyncio.gather()`. The helper `_print_stream()` consumes one generator at a time while the other keeps arriving. |

> **Why `asyncio.gather`?**  
> It allows the event loop to interleave the two streams: when one stream waits for the next byte from the network it gives the loop a chance to serve the other stream. Without concurrency the second stream would block the first until it completes.

---

## 3️⃣ Customizations

| Feature | Where to tweak |
|---------|-----------------|
| **Model** | Change `MODEL = "openrouter/o1-mini"` or pass a different ID to `stream_chat`. |
| **Temperature / top_p** | Adjust the named arguments of `stream_chat`. |
| **Prompt** | Edit `messages1` / `messages2` or build a larger conversation. |
| **Post‑processing** | Receive the raw delta objects and do your own formatting, token‑counting, or storage. |
| **Retry logic** | Wrap the request in `httpx.retry()` or add your own back‑off. |
| **Timeout** | Pass a `timeout` argument to `AsyncClient` or to the `stream()` call. |

---

## 4️⃣ What to expect in the console

```
[Chat‑1]: Hello! I'm fine, thanks for asking.
[Chat‑2]: Why shouldn't a cat go to the bank?  
[Chat‑1]: Are you looking for a simple yes, or...  
[Chat‑2]: ...to take a \"purr\" of all the interest!  
[Chat‑1]: That's a good one!  
------------------------------------------------
```

Tokens (or token fragments) appear as soon as they arrive – nothing is buffered until the entire response finishes. The `"[DONE]"` marker signals the end of the stream.

---

## 5️⃣ Common pitfalls

| Problem | Fix |
|---------|-----|
| **Blank env variable** | Confirm `OPENROUTER_API_KEY` spelling and export. |
| **Rate‑limit errors** | Handle 429 responses (`resp.raise_for_status()` will raise); implement exponential back‑off. |
| **Mismatched SSE line** | Ensure you strip whitespace; lines that don’t start with `"data: "` are ignored. |
| **Large outputs** | If you want each full sentence instead of raw delta, accumulate into a buffer and flush on newline (`"\n"`). |

---

Happy hacking! 🚀 If you’d like to see a variation that uses `asyncio.Queue` for more complex orchestration, let me know.

## Reasoning:
Below is a **stand‑alone, ready‑to‑run** example that shows how to

| ✅ | Feature |
|----|---------|
| 🔥 | Call OpenRouter’s chat‑completion endpoint as a **streaming** request |
| 🌐 | Use **httpx.AsyncClient** (no `aiohttp` needed) |
| 🚀 | Fire two independent streams in parallel with `asyncio.gather` |
| 🔀 | Consume the stream token‑by‑token and print it live |

> **Prerequisites**  
> ```bash
> pip install httpx==0.27.*
> export OPENROUTER_API_KEY="YOUR_OPENROUTER_KEY"   # or set it in your env
> ```

---

## 1️⃣ The complete script

```python
#!/usr/bin/env python3
"""async_stream_chat.py – Stream multiple LLM chat responses with httpx + asyncio"""

import os
import json
import asyncio
from typing import AsyncGenerator, List, Dict

import httpx

# --------------------------------------------------------------------------
# Configuration & helpers
# --------------------------------------------------------------------------

API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise RuntimeError(
        "Please set the OPENROUTER_API_KEY environment variable to your key."
    )

BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "openrouter/o1-mini"  # change to any supported model

HEADERS: Dict[str, str] = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    # OpenRouter distinguishes streaming by this accept header
    "Accept": "text/event-stream",
}


async def stream_chat(
    client: httpx.AsyncClient,
    messages: List[Dict[str, str]],
    *,
    model: str = MODEL,
    temperature: float = 0.7,
    top_p: float = 1.0,
) -> AsyncGenerator[str, None]:
    """
    Yield tokens (content strings) from the model as they arrive.

    :param client: Re‑used AsyncClient – share connections across calls
    :param messages: List of OpenAI‑style message dicts
    :param model: Model ID
    :param temperature: Sampler temperature
    :param top_p: Top‑p nucleus sampling
    :yield: ``str`` – a chunk of the generated text
    """
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "top_p": top_p,
        "stream": True,
    }

    # OpenRouter expects a streamed response as a Server‑Sent Events (SSE) stream.
    async with client.stream(
        "POST", f"{BASE_URL}/chat/completions", json=payload, headers=HEADERS
    ) as resp:
        resp.raise_for_status()

        async for line in resp.aiter_lines():
            if not line:
                continue
            # Each non‑empty line looks like: data: {"choices":[{"delta":{"content":"..."}},...}]
            if line.startswith("data: "):
                raw = line[6:].strip()
                if raw == "[DONE]":
                    break
                try:
                    data = json.loads(raw)
                except json.JSONDecodeError:
                    continue  # skip malformed lines

                # open router follows the ChatCompletionDelta schema
                for choice in data.get("choices", []):
                    delta = choice.get("delta", {})
                    if "content" in delta:
                        yield delta["content"]


# --------------------------------------------------------------------------
# Running several streams in parallel
# --------------------------------------------------------------------------


async def _print_stream(
    task: AsyncGenerator[str, None],  # the stream generator
    label: str,  # label for the console
) -> None:
    """Consume a stream and echo it to the console."""
    async for token in task:
        print(f"[{label}]: {token}", end="", flush=True)
    print("\n" + "-" * 40)


async def main() -> None:
    """
    Fire two independent chat streams and watch their output live.
    Feel free to replace the messages with your own prompts.
    """
    messages1 = [{"role": "user", "content": "Hello, how are you?"}]
    messages2 = [{"role": "user", "content": "Tell me a joke about cats."}]

    async with httpx.AsyncClient() as client:
        # Create stream generators but *don't* start consuming yet
        stream1 = stream_chat(client, messages1)
        stream2 = stream_chat(client, messages2)

        # Now run both streams concurrently
        await asyncio.gather(
            _print_stream(stream1, "Chat‑1"),
            _print_stream(stream2, "Chat‑2"),
        )


# --------------------------------------------------------------------------
# Entrypoint
# --------------------------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 2️⃣ How it works

| Step | What happens |
|------|--------------|
| **HTTP client** | `httpx.AsyncClient()` keeps an HTTP/2 connection pool open, so two requests reuse the same socket. |
| **Endpoint** | `POST /chat/completions` with `"stream": true`. |
| **Headers** | `Accept: text/event-stream` tells OpenRouter we want a Server‑Sent Events (SSE) stream. |
| **Streaming** | `client.stream()` returns an async context manager that yields each received network line via `aiter_lines()`. |
| **SSE parsing** | We strip the `"data: "` prefix, skip `"[DONE]"`, parse the JSON, and yield the `content` field from each `delta` object. |
| **Parallelism** | Two generator objects (`stream1`, `stream2`) are passed to `asyncio.gather()`. The helper `_print_stream()` consumes one generator at a time while the other keeps arriving. |

> **Why `asyncio.gather`?**  
> It allows the event loop to interleave the two streams: when one stream waits for the next byte from the network it gives the loop a chance to serve the other stream. Without concurrency the second stream would block the first until it completes.

---

## 3️⃣ Customizations

| Feature | Where to tweak |
|---------|-----------------|
| **Model** | Change `MODEL = "openrouter/o1-mini"` or pass a different ID to `stream_chat`. |
| **Temperature / top_p** | Adjust the named arguments of `stream_chat`. |
| **Prompt** | Edit `messages1` / `messages2` or build a larger conversation. |
| **Post‑processing** | Receive the raw delta objects and do your own formatting, token‑counting, or storage. |
| **Retry logic** | Wrap the request in `httpx.retry()` or add your own back‑off. |
| **Timeout** | Pass a `timeout` argument to `AsyncClient` or to the `stream()` call. |

---

## 4️⃣ What to expect in the console

```
[Chat‑1]: Hello! I'm fine, thanks for asking.
[Chat‑2]: Why shouldn't a cat go to the bank?  
[Chat‑1]: Are you looking for a simple yes, or...  
[Chat‑2]: ...to take a \"purr\" of all the interest!  
[Chat‑1]: That's a good one!  
------------------------------------------------
```

Tokens (or token fragments) appear as soon as they arrive – nothing is buffered until the entire response finishes. The `"[DONE]"` marker signals the end of the stream.

---

## 5️⃣ Common pitfalls

| Problem | Fix |
|---------|-----|
| **Blank env variable** | Confirm `OPENROUTER_API_KEY` spelling and export. |
| **Rate‑limit errors** | Handle 429 responses (`resp.raise_for_status()` will raise); implement exponential back‑off. |
| **Mismatched SSE line** | Ensure you strip whitespace; lines that don’t start with `"data: "` are ignored. |
| **Large outputs** | If you want each full sentence instead of raw delta, accumulate into a buffer and flush on newline (`"\n"`). |

---

Happy hacking! 🚀 If you’d like to see a variation that uses `asyncio.Queue` for more complex orchestration, let me know.
