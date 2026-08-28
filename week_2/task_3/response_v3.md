
# Prompt: give the program to chat to the llm in openrouter as API request using httpx and need to implement the async with batch of prompts

## Response:
Below is a **complete, self‑contained Python example** that talks to the OpenRouter LLM API with `httpx` **asynchronously** and processes a *batch* of prompts in parallel.

> **What this script does**  
> * Builds a single request body for each prompt.  
> * Uses `httpx.AsyncClient` to call `https://openrouter.ai/api/v1/chat/completions`.  
> * Limits the number of concurrent requests with an `asyncio.Semaphore` (you can tweak `batch_size`).  
> * Collects all replies and prints them out.

You only need to set your OpenRouter API key in the environment (`OPENROUTER_API_KEY`).  The rest of the code is ready to run.

```python
#!/usr/bin/env python3
"""chat_to_openrouter.py

Send a batch of prompts to OpenRouter's chat API asynchronously using httpx.

Requirements:
    - python ≥ 3.9
    - httpx 0.27+
"""

from __future__ import annotations

import os
import asyncio
import json
from typing import List, Dict, Any

import httpx


# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

OPENROUTER_API_KEY: str | None = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise RuntimeError(
        "Missing environment variable OPENROUTER_API_KEY. "
        "Set it to your OpenRouter API key before running the script."
    )

# Endpoint for chat completions – change it if the API moves.
WHISPER_ENDPOINT: str = "https://openrouter.ai/api/v1/chat/completions"

HEADERS: Dict[str, str] = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    # Optional extra header – adjust if the service requires more.
}

# Model you want to use – replace with your favourite model string.
DEFAULT_MODEL: str = "gpt-4o-mini"

# --------------------------------------------------------------------------- #
# Async helpers
# --------------------------------------------------------------------------- #


async def _chat(
    client: httpx.AsyncClient,
    prompt: str,
    *,
    model: str = DEFAULT_MODEL,
    max_tokens: int = 4096,
    temperature: float = 0.7,
) -> str:
    """Send a single prompt and return the assistant's message text."""
    payload: Dict[str, Any] = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": temperature,
        # Uncomment the following line if you want streaming responses.
        # "stream": True,
    }

    # The `timeout` can be tuned; 30 s usually works for a single prompt.
    try:
        response = await client.post(
            WHISPER_ENDPOINT,
            headers=HEADERS,
            json=payload,
            timeout=30.0,
        )
        response.raise_for_status()  # Raise for HTTP errors (4xx/5xx)
    except httpx.HTTPStatusError as exc:
        # `exc.response` holds the server’s reply
        status = exc.response.status_code
        content = exc.response.text[:200]  # truncate large bodies
        raise RuntimeError(
            f"OpenRouter API returned {status} for prompt {prompt!r}: {content}"
        ) from exc
    except httpx.RequestError as exc:  # network-related error
        raise RuntimeError(f"Network error for prompt {prompt!r}: {exc}") from exc

    # Parse the response – the shape matches OpenAI’s chat‑format.
    data = response.json()
    try:
        # A typical OpenAI‑compatible response:
        # {"choices":[{"message":{"role":"assistant","content":"…"}}],...}
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError) as exc:
        # Unexpected payload shape
        raise RuntimeError(
            f"Unexpected response structure for prompt {prompt!r}: {json.dumps(data, indent=2)}"
        ) from exc


async def batch_prompts(
    prompts: List[str],
    *,
    batch_size: int = 5,
    model: str = DEFAULT_MODEL,
) -> List[str]:
    """
    Send a whole list of prompts to OpenRouter in parallel, limited by `batch_size`.

    Parameters
    ----------
    prompts: List[str]
        List of user prompts to send.
    batch_size: int
        Maximum number of requests that may run concurrently.
    model: str
        LLM model string to ask the API to use.

    Returns
    -------
    List[str]
        Corresponding assistant replies in the same order as `prompts`.
    """
    results: List[str] = []

    # A single HTTP client lets us reuse the TCP connection.
    async with httpx.AsyncClient(http2=True, timeout=30.0) as client:
        semaphore = asyncio.Semaphore(batch_size)

        async def _sem_chat(prompt: str) -> str:
            async with semaphore:
                return await _chat(client, prompt, model=model)

        # Fire one task per prompt, but only `batch_size` run at a time.
        tasks = [asyncio.create_task(_sem_chat(p)) for p in prompts]

        # Preserve order by awaiting tasks in the order we created them.
        for task in tasks:
            results.append(await task)

    return results


# --------------------------------------------------------------------------- #
# Demo / entry point
# --------------------------------------------------------------------------- #


async def main() -> None:
    # Example: read prompts from a text file (one per line).
    # Or hard‑code a list, or read from stdin, etc.
    # Here we just hard‑code 5 demo prompts.
    demo_prompts: List[str] = [
        "Tell me a joke about programming.",
        "Explain the concept of async/await in Python in a short paragraph.",
        "What are the differences between HTTP/1.1 and HTTP/2?",
        "Write a short poem about the ocean.",
        "Translate 'Hello, world!' into Spanish.",
    ]

    print(f"Sending {len(demo_prompts)} prompts in batches of up to 3…")
    replies = await batch_prompts(
        demo_prompts,
        batch_size=3,  # Max 3 concurrent requests
        model="gpt-4o-mini",  # You can change to a different model if you wish.
    )

    for i, (inp, out) in enumerate(zip(demo_prompts, replies), start=1):
        print(f"\n--- Prompt {i} ---")
        print(f"Q: {inp}")
        print(f"A: {out}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
```

### How it works

| Piece of code | What it does |
|--------------|--------------|
| `httpx.AsyncClient` | Reuses a single connection for all requests → less latency |
| `asyncio.Semaphore` | Caps the amount of parallel in‑flight requests – avoid being rate‑limited or overloading your client |
| `asyncio.create_task` / `await` | Fire off all tasks, then gather the replies while preserving original order |
| Error handling | `httpx.HTTPStatusError` → non‑200 status codes, `httpx.RequestError` → network problems. Custom `RuntimeError`s give you a clear log. |
| `HEADERS` | Must contain `Authorization: Bearer <key>` and `Content-Type: application/json`. |
| `payload` | Uses the chat‑completions format similar to OpenAI. You can tweak `max_tokens`, `temperature`, `stream`, etc. |
| `batch_size` | Default of 5 but you can bump it to reduce round‑trip time if the API allows it. |

> **Tip:** If you need **streaming** responses (i.e., incremental token output), uncomment the `"stream": True` line and adjust the response handling to read the event stream (`client.stream(...)`).  

Feel free to hook this into a larger application (e.g., a FastAPI endpoint that submits a set of prompts, or a CLI tool).  The same pattern scales to hundreds of prompts – just remember to keep `batch_size` within the OpenRouter rate‑limits for your token plan. Happy experimenting!

## Reasoning:
Below is a **complete, self‑contained Python example** that talks to the OpenRouter LLM API with `httpx` **asynchronously** and processes a *batch* of prompts in parallel.

> **What this script does**  
> * Builds a single request body for each prompt.  
> * Uses `httpx.AsyncClient` to call `https://openrouter.ai/api/v1/chat/completions`.  
> * Limits the number of concurrent requests with an `asyncio.Semaphore` (you can tweak `batch_size`).  
> * Collects all replies and prints them out.

You only need to set your OpenRouter API key in the environment (`OPENROUTER_API_KEY`).  The rest of the code is ready to run.

```python
#!/usr/bin/env python3
"""chat_to_openrouter.py

Send a batch of prompts to OpenRouter's chat API asynchronously using httpx.

Requirements:
    - python ≥ 3.9
    - httpx 0.27+
"""

from __future__ import annotations

import os
import asyncio
import json
from typing import List, Dict, Any

import httpx


# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

OPENROUTER_API_KEY: str | None = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise RuntimeError(
        "Missing environment variable OPENROUTER_API_KEY. "
        "Set it to your OpenRouter API key before running the script."
    )

# Endpoint for chat completions – change it if the API moves.
WHISPER_ENDPOINT: str = "https://openrouter.ai/api/v1/chat/completions"

HEADERS: Dict[str, str] = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    # Optional extra header – adjust if the service requires more.
}

# Model you want to use – replace with your favourite model string.
DEFAULT_MODEL: str = "gpt-4o-mini"

# --------------------------------------------------------------------------- #
# Async helpers
# --------------------------------------------------------------------------- #


async def _chat(
    client: httpx.AsyncClient,
    prompt: str,
    *,
    model: str = DEFAULT_MODEL,
    max_tokens: int = 4096,
    temperature: float = 0.7,
) -> str:
    """Send a single prompt and return the assistant's message text."""
    payload: Dict[str, Any] = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": temperature,
        # Uncomment the following line if you want streaming responses.
        # "stream": True,
    }

    # The `timeout` can be tuned; 30 s usually works for a single prompt.
    try:
        response = await client.post(
            WHISPER_ENDPOINT,
            headers=HEADERS,
            json=payload,
            timeout=30.0,
        )
        response.raise_for_status()  # Raise for HTTP errors (4xx/5xx)
    except httpx.HTTPStatusError as exc:
        # `exc.response` holds the server’s reply
        status = exc.response.status_code
        content = exc.response.text[:200]  # truncate large bodies
        raise RuntimeError(
            f"OpenRouter API returned {status} for prompt {prompt!r}: {content}"
        ) from exc
    except httpx.RequestError as exc:  # network-related error
        raise RuntimeError(f"Network error for prompt {prompt!r}: {exc}") from exc

    # Parse the response – the shape matches OpenAI’s chat‑format.
    data = response.json()
    try:
        # A typical OpenAI‑compatible response:
        # {"choices":[{"message":{"role":"assistant","content":"…"}}],...}
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError) as exc:
        # Unexpected payload shape
        raise RuntimeError(
            f"Unexpected response structure for prompt {prompt!r}: {json.dumps(data, indent=2)}"
        ) from exc


async def batch_prompts(
    prompts: List[str],
    *,
    batch_size: int = 5,
    model: str = DEFAULT_MODEL,
) -> List[str]:
    """
    Send a whole list of prompts to OpenRouter in parallel, limited by `batch_size`.

    Parameters
    ----------
    prompts: List[str]
        List of user prompts to send.
    batch_size: int
        Maximum number of requests that may run concurrently.
    model: str
        LLM model string to ask the API to use.

    Returns
    -------
    List[str]
        Corresponding assistant replies in the same order as `prompts`.
    """
    results: List[str] = []

    # A single HTTP client lets us reuse the TCP connection.
    async with httpx.AsyncClient(http2=True, timeout=30.0) as client:
        semaphore = asyncio.Semaphore(batch_size)

        async def _sem_chat(prompt: str) -> str:
            async with semaphore:
                return await _chat(client, prompt, model=model)

        # Fire one task per prompt, but only `batch_size` run at a time.
        tasks = [asyncio.create_task(_sem_chat(p)) for p in prompts]

        # Preserve order by awaiting tasks in the order we created them.
        for task in tasks:
            results.append(await task)

    return results


# --------------------------------------------------------------------------- #
# Demo / entry point
# --------------------------------------------------------------------------- #


async def main() -> None:
    # Example: read prompts from a text file (one per line).
    # Or hard‑code a list, or read from stdin, etc.
    # Here we just hard‑code 5 demo prompts.
    demo_prompts: List[str] = [
        "Tell me a joke about programming.",
        "Explain the concept of async/await in Python in a short paragraph.",
        "What are the differences between HTTP/1.1 and HTTP/2?",
        "Write a short poem about the ocean.",
        "Translate 'Hello, world!' into Spanish.",
    ]

    print(f"Sending {len(demo_prompts)} prompts in batches of up to 3…")
    replies = await batch_prompts(
        demo_prompts,
        batch_size=3,  # Max 3 concurrent requests
        model="gpt-4o-mini",  # You can change to a different model if you wish.
    )

    for i, (inp, out) in enumerate(zip(demo_prompts, replies), start=1):
        print(f"\n--- Prompt {i} ---")
        print(f"Q: {inp}")
        print(f"A: {out}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
```

### How it works

| Piece of code | What it does |
|--------------|--------------|
| `httpx.AsyncClient` | Reuses a single connection for all requests → less latency |
| `asyncio.Semaphore` | Caps the amount of parallel in‑flight requests – avoid being rate‑limited or overloading your client |
| `asyncio.create_task` / `await` | Fire off all tasks, then gather the replies while preserving original order |
| Error handling | `httpx.HTTPStatusError` → non‑200 status codes, `httpx.RequestError` → network problems. Custom `RuntimeError`s give you a clear log. |
| `HEADERS` | Must contain `Authorization: Bearer <key>` and `Content-Type: application/json`. |
| `payload` | Uses the chat‑completions format similar to OpenAI. You can tweak `max_tokens`, `temperature`, `stream`, etc. |
| `batch_size` | Default of 5 but you can bump it to reduce round‑trip time if the API allows it. |

> **Tip:** If you need **streaming** responses (i.e., incremental token output), uncomment the `"stream": True` line and adjust the response handling to read the event stream (`client.stream(...)`).  

Feel free to hook this into a larger application (e.g., a FastAPI endpoint that submits a set of prompts, or a CLI tool).  The same pattern scales to hundreds of prompts – just remember to keep `batch_size` within the OpenRouter rate‑limits for your token plan. Happy experimenting!
