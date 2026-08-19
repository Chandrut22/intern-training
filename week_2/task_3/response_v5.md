# Prompt: give the program to chat to the llm in openrouter as API request using httpx and need to implement the async and i need to stream the llm and  user give the input prompt and print the token usage, cost, model name for every chat

## Response:

Below is a **fully‑working, vanilla Python 3.10+ example** that

| Feature                              | How it’s handled                                                                  |
| ------------------------------------ | ---------------------------------------------------------------------------------- |
| **Async**                      | Uses`asyncio` + `httpx.AsyncClient`                                            |
| **Streaming**                  | SSE‑style streaming (the same format that the OpenRouter API uses)                |
| **User prompt**                | Terminal prompt – keep feeding new questions until you type`:quit`              |
| **Token usage / cost / model** | Collected from the final JSON chunk that OpenRouter sends at the end of the stream |

> **What you’ll need**
>
> 1. **Python 3.10 or later**
> 2. `pip install httpx[http2]` – we use the HTTP/2 support that is nice for streaming.
> 3. An **OpenRouter API key** (set it in an environment variable ``OPENROUTER_API_KEY`` or enter it at runtime).

---

## 1️⃣  The complete script

```python
#!/usr/bin/env python3
"""
Async chat with OpenRouter – streaming + token usage + cost.

Usage
-----
1️⃣  pip install httpx[http2]
2️⃣  export OPENROUTER_API_KEY="pk_…"
3️⃣  python openrouter_chat.py

(Or keep the key in your shell/OS env as shown.)

"""

import asyncio
import json
import os
from typing import Any, Dict, Optional

import httpx


# --------------------------------------------------------------------------- #
# Config – change the model or other defaults if you want.
# --------------------------------------------------------------------------- #
BASE_URL: str = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL: str = "openai/gpt-4o-mini"  # e.g. "gpt-4o-mini" through OpenRouter
DEFAULT_TEMP: float = 0.7
DEFAULT_MAX_TOKENS: int = 500

# --------------------------------------------------------------------------- #
# Helper: Simple wrapper to parse the streaming data lines.
# --------------------------------------------------------------------------- #
def _extract_json_from_line(line: str) -> Optional[Dict[str, Any]]:
    """
    OpenRouter streams lines that look like:

        data: { ...json... }

    The function chops it off and parses the JSON payload.
    """
    line = line.strip()
    if not line or not line.startswith("data:"):
        return None
    # OpenRouter may send the "data: [DONE]" line at the end
    if line == "data: [DONE]":
        return {"done": True}
    payload = line[5:].strip()  # after 'data: '
    try:
        return json.loads(payload)
    except json.JSONDecodeError:
        return None


# --------------------------------------------------------------------------- #
# The core async logic: streaming a single completion.
# --------------------------------------------------------------------------- #
async def stream_completion(
    client: httpx.AsyncClient,
    prompt: str,
    model: str = DEFAULT_MODEL,
) -> None:
    """
    Send the prompt to OpenRouter, stream the answer in real time,
    and print token‑usage/cost/model info once the stream ends.
    """
    # Build the request payload
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": True,
        "max_tokens": DEFAULT_MAX_TOKENS,
        "temperature": DEFAULT_TEMP,
    }

    headers = {
        "Content-Type": "application/json",
        # OpenRouter expects the key in the standard Bearer format
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
    }

    # ----------------------------------------------------------- #
    # Calling the API
    # ----------------------------------------------------------- #
    try:
        async with client.stream("POST", BASE_URL, json=payload, headers=headers) as resp:
            resp.raise_for_status()

            usage: Optional[Dict[str, Any]] = None
            model_name: Optional[str] = None
            total_cost: Optional[float] = None

            # Streaming: each line is either a delta or the final DONE marker
            async for raw_line in resp.aiter_text():
                data = _extract_json_from_line(raw_line)
                if data is None:
                    continue
                if data.get("done"):  # streamed when OpenRouter sends [DONE]
                    break

                # 1️⃣  The heart of OpenAI‑style streaming
                if "choices" in data:
                    for choice in data["choices"]:
                        # a) The content delta
                        delta = choice.get("delta", {})
                        if text := delta.get("content"):
                            # Print as soon we receive it
                            print(text, end="", flush=True)

                        # b) Metadata that is only available at the very end (if OpenRouter includes it)
                        if usage_data := data.get("usage"):
                            usage = usage_data
                        if cost_data := data.get("total_cost"):          # new field
                            total_cost = float(cost_data)
                        if model_data := data.get("model"):
                            model_name = model_data

            # --------------------------------------------------- #
            # At this point the stream is finished.  Print a line break.
            # --------------------------------------------------- #
            print("\n\n--- Completion finished ---")

            # 2️⃣ Show any usage / cost details that were sent with the last chunk
            if usage:
                print(f"✨ Token usage: {usage}")
            if total_cost is not None:
                print(f"💰 Total cost: ${total_cost:.6f}")
            if model_name:
                print(f"🤖 Model used: {model_name}")

    except httpx.HTTPStatusError as exc:
        # Show the error body so the user knows what went wrong.
        print(f"\n❌ HTTP Error {exc.response.status_code}: {exc.response.text}")
    except httpx.HTTPError as exc:
        # Network‑level errors etc.
        print(f"\n❌ Network error: {exc}")


# --------------------------------------------------------------------------- #
# Interactive loop – keep asking for a new prompt until the user quits.
# --------------------------------------------------------------------------- #
async def main() -> None:
    """
    Simple REPL that:
    1. Asks the user for a prompt.
    2. Streams the response and prints usage/cost.
    3. Loops until the user types ':quit'.
    """
    # Quick environment‑var check
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        api_key = input("❗️ No OPENROUTER_API_KEY in env – enter it now: ").strip()
        if not api_key:
            raise RuntimeError("You need an API key to keep going.")
        os.environ["OPENROUTER_API_KEY"] = api_key

    print(
        "🚀 OpenRouter streaming demo. Type ':quit' to exit.\n"
        f"Using model: {DEFAULT_MODEL} (you can change it by editing the source).\n"
    )

    async with httpx.AsyncClient(http2=True) as client:
        while True:
            prompt = input("\n👉 You: ").strip()
            if not prompt:
                continue
            if prompt.lower() in {":quit", "quit", "exit"}:
                print("👋 Goodbye!")
                break

            print("\n🗣️  Assistant (streaming):")
            await stream_completion(client, prompt, model=DEFAULT_MODEL)


# --------------------------------------------------------------------------- #
# The usual asyncio guard
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    asyncio.run(main())
```

---

## 2️⃣  What’s happening under the hood?

| Step                              | Implementation detail                                                                                                                   | Why it matters                                                                                                              |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **Async call**              | `async with client.stream(...):`                                                                                                      | Makes the HTTP request*without blocking* the event loop, enabling true concurrency.                                       |
| **Streaming**               | `async for raw_line in resp.aiter_text():`                                                                                            | Works with**SSE**‑style data (`data: …`). Each chunk is parsed and immediately printed.                           |
| **Token / cost extraction** | Inside the loop we look for`"usage"`, `"total_cost"`, and `"model"` fields in the JSON that the service emits as the final block. | These fields are only present at the end of the stream, so we keep the latest values and print them once the stream closes. |
| **Graceful exit**           | `resp.raise_for_status()` + `except httpx.HTTPStatusError`                                                                          | Gives you a helpful error message if you end up using an invalid model, exceeding your quota, etc.                          |
| **Environment‑variable**   | `OPENROUTER_API_KEY`                                                                                                                  | Keeps your key out of the source code; you can also paste it in when prompted.                                              |

---

## 3️⃣  Testing & Tweaking

- **Switch model** – change `DEFAULT_MODEL` at the top of the script to any OpenRouter‑available model (e.g. `"openai/gpt-4o-mini"` or `"anthropic/claude-3-5-sonnet-20240620"`).
- **Temperature / max tokens** – edit `DEFAULT_TEMP` and `DEFAULT_MAX_TOKENS`.
- **Add more context** – modify the payload `messages` array to pre‑populate the chat with system‑level instructions.

---

## 4️⃣  Gotchas

1. **OpenRouter’s Streaming Format**Some older OpenRouter deployments use a slightly different SSE format, or an extra newline before the first `data:` line. The helper `_extract_json_from_line` is tolerant – it just looks for `"data:"`.
2. **Cost & Usage**Not every OpenRouter plan reports `total_cost` in the streamed payload. If you don’t see it, you may need to run a non‑streaming request to retrieve the cost, or inspect the platform dashboard.
3. **Rate‑limits**The OpenRouter API may limit you to a few requests/sec. The demo above doesn’t handle back‑pressure; if you hit a 429 you’ll see an error message and can retry manually.
4. **HTTP/2**
   We set `http2=True` in the `AsyncClient` – the OpenRouter API shines on HTTP/2. If you’re on an older environment that can’t talk HTTP/2, drop that flag – it will fall back to HTTP/1.1.

---

### 🎉  Happy streaming!

Save the script to e.g. `openrouter_chat.py`, run it, feed it a prompt, and watch the tokens roll out in real time while you’re informed of the cost and token usage once the answer is finished. 🚀

## Reasoning:

Below is a **fully‑working, vanilla Python 3.10+ example** that

| Feature                              | How it’s handled                                                                  |
| ------------------------------------ | ---------------------------------------------------------------------------------- |
| **Async**                      | Uses`asyncio` + `httpx.AsyncClient`                                            |
| **Streaming**                  | SSE‑style streaming (the same format that the OpenRouter API uses)                |
| **User prompt**                | Terminal prompt – keep feeding new questions until you type`:quit`              |
| **Token usage / cost / model** | Collected from the final JSON chunk that OpenRouter sends at the end of the stream |

> **What you’ll need**
>
> 1. **Python 3.10 or later**
> 2. `pip install httpx[http2]` – we use the HTTP/2 support that is nice for streaming.
> 3. An **OpenRouter API key** (set it in an environment variable ``OPENROUTER_API_KEY`` or enter it at runtime).

---

## 1️⃣  The complete script

```python
#!/usr/bin/env python3
"""
Async chat with OpenRouter – streaming + token usage + cost.

Usage
-----
1️⃣  pip install httpx[http2]
2️⃣  export OPENROUTER_API_KEY="pk_…"
3️⃣  python openrouter_chat.py

(Or keep the key in your shell/OS env as shown.)

"""

import asyncio
import json
import os
from typing import Any, Dict, Optional

import httpx


# --------------------------------------------------------------------------- #
# Config – change the model or other defaults if you want.
# --------------------------------------------------------------------------- #
BASE_URL: str = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL: str = "openai/gpt-4o-mini"  # e.g. "gpt-4o-mini" through OpenRouter
DEFAULT_TEMP: float = 0.7
DEFAULT_MAX_TOKENS: int = 500

# --------------------------------------------------------------------------- #
# Helper: Simple wrapper to parse the streaming data lines.
# --------------------------------------------------------------------------- #
def _extract_json_from_line(line: str) -> Optional[Dict[str, Any]]:
    """
    OpenRouter streams lines that look like:

        data: { ...json... }

    The function chops it off and parses the JSON payload.
    """
    line = line.strip()
    if not line or not line.startswith("data:"):
        return None
    # OpenRouter may send the "data: [DONE]" line at the end
    if line == "data: [DONE]":
        return {"done": True}
    payload = line[5:].strip()  # after 'data: '
    try:
        return json.loads(payload)
    except json.JSONDecodeError:
        return None


# --------------------------------------------------------------------------- #
# The core async logic: streaming a single completion.
# --------------------------------------------------------------------------- #
async def stream_completion(
    client: httpx.AsyncClient,
    prompt: str,
    model: str = DEFAULT_MODEL,
) -> None:
    """
    Send the prompt to OpenRouter, stream the answer in real time,
    and print token‑usage/cost/model info once the stream ends.
    """
    # Build the request payload
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": True,
        "max_tokens": DEFAULT_MAX_TOKENS,
        "temperature": DEFAULT_TEMP,
    }

    headers = {
        "Content-Type": "application/json",
        # OpenRouter expects the key in the standard Bearer format
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
    }

    # ----------------------------------------------------------- #
    # Calling the API
    # ----------------------------------------------------------- #
    try:
        async with client.stream("POST", BASE_URL, json=payload, headers=headers) as resp:
            resp.raise_for_status()

            usage: Optional[Dict[str, Any]] = None
            model_name: Optional[str] = None
            total_cost: Optional[float] = None

            # Streaming: each line is either a delta or the final DONE marker
            async for raw_line in resp.aiter_text():
                data = _extract_json_from_line(raw_line)
                if data is None:
                    continue
                if data.get("done"):  # streamed when OpenRouter sends [DONE]
                    break

                # 1️⃣  The heart of OpenAI‑style streaming
                if "choices" in data:
                    for choice in data["choices"]:
                        # a) The content delta
                        delta = choice.get("delta", {})
                        if text := delta.get("content"):
                            # Print as soon we receive it
                            print(text, end="", flush=True)

                        # b) Metadata that is only available at the very end (if OpenRouter includes it)
                        if usage_data := data.get("usage"):
                            usage = usage_data
                        if cost_data := data.get("total_cost"):          # new field
                            total_cost = float(cost_data)
                        if model_data := data.get("model"):
                            model_name = model_data

            # --------------------------------------------------- #
            # At this point the stream is finished.  Print a line break.
            # --------------------------------------------------- #
            print("\n\n--- Completion finished ---")

            # 2️⃣ Show any usage / cost details that were sent with the last chunk
            if usage:
                print(f"✨ Token usage: {usage}")
            if total_cost is not None:
                print(f"💰 Total cost: ${total_cost:.6f}")
            if model_name:
                print(f"🤖 Model used: {model_name}")

    except httpx.HTTPStatusError as exc:
        # Show the error body so the user knows what went wrong.
        print(f"\n❌ HTTP Error {exc.response.status_code}: {exc.response.text}")
    except httpx.HTTPError as exc:
        # Network‑level errors etc.
        print(f"\n❌ Network error: {exc}")


# --------------------------------------------------------------------------- #
# Interactive loop – keep asking for a new prompt until the user quits.
# --------------------------------------------------------------------------- #
async def main() -> None:
    """
    Simple REPL that:
    1. Asks the user for a prompt.
    2. Streams the response and prints usage/cost.
    3. Loops until the user types ':quit'.
    """
    # Quick environment‑var check
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        api_key = input("❗️ No OPENROUTER_API_KEY in env – enter it now: ").strip()
        if not api_key:
            raise RuntimeError("You need an API key to keep going.")
        os.environ["OPENROUTER_API_KEY"] = api_key

    print(
        "🚀 OpenRouter streaming demo. Type ':quit' to exit.\n"
        f"Using model: {DEFAULT_MODEL} (you can change it by editing the source).\n"
    )

    async with httpx.AsyncClient(http2=True) as client:
        while True:
            prompt = input("\n👉 You: ").strip()
            if not prompt:
                continue
            if prompt.lower() in {":quit", "quit", "exit"}:
                print("👋 Goodbye!")
                break

            print("\n🗣️  Assistant (streaming):")
            await stream_completion(client, prompt, model=DEFAULT_MODEL)


# --------------------------------------------------------------------------- #
# The usual asyncio guard
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    asyncio.run(main())
```

---

## 2️⃣  What’s happening under the hood?

| Step                              | Implementation detail                                                                                                                   | Why it matters                                                                                                              |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **Async call**              | `async with client.stream(...):`                                                                                                      | Makes the HTTP request*without blocking* the event loop, enabling true concurrency.                                       |
| **Streaming**               | `async for raw_line in resp.aiter_text():`                                                                                            | Works with**SSE**‑style data (`data: …`). Each chunk is parsed and immediately printed.                           |
| **Token / cost extraction** | Inside the loop we look for`"usage"`, `"total_cost"`, and `"model"` fields in the JSON that the service emits as the final block. | These fields are only present at the end of the stream, so we keep the latest values and print them once the stream closes. |
| **Graceful exit**           | `resp.raise_for_status()` + `except httpx.HTTPStatusError`                                                                          | Gives you a helpful error message if you end up using an invalid model, exceeding your quota, etc.                          |
| **Environment‑variable**   | `OPENROUTER_API_KEY`                                                                                                                  | Keeps your key out of the source code; you can also paste it in when prompted.                                              |

---

## 3️⃣  Testing & Tweaking

- **Switch model** – change `DEFAULT_MODEL` at the top of the script to any OpenRouter‑available model (e.g. `"openai/gpt-4o-mini"` or `"anthropic/claude-3-5-sonnet-20240620"`).
- **Temperature / max tokens** – edit `DEFAULT_TEMP` and `DEFAULT_MAX_TOKENS`.
- **Add more context** – modify the payload `messages` array to pre‑populate the chat with system‑level instructions.

---

## 4️⃣  Gotchas

1. **OpenRouter’s Streaming Format**Some older OpenRouter deployments use a slightly different SSE format, or an extra newline before the first `data:` line. The helper `_extract_json_from_line` is tolerant – it just looks for `"data:"`.
2. **Cost & Usage**Not every OpenRouter plan reports `total_cost` in the streamed payload. If you don’t see it, you may need to run a non‑streaming request to retrieve the cost, or inspect the platform dashboard.
3. **Rate‑limits**The OpenRouter API may limit you to a few requests/sec. The demo above doesn’t handle back‑pressure; if you hit a 429 you’ll see an error message and can retry manually.
4. **HTTP/2**
   We set `http2=True` in the `AsyncClient` – the OpenRouter API shines on HTTP/2. If you’re on an older environment that can’t talk HTTP/2, drop that flag – it will fall back to HTTP/1.1.

---

### 🎉  Happy streaming!

Save the script to e.g. `openrouter_chat.py`, run it, feed it a prompt, and watch the tokens roll out in real time while you’re informed of the cost and token usage once the answer is finished. 🚀
